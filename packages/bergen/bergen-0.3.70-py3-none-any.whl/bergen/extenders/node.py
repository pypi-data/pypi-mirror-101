
import asyncio
from asyncio.futures import Future
from bergen.postmans.base import NodeException
from bergen.utils import expandOutputs, shrinkInputs
from bergen.monitor.monitor import Monitor
from bergen.messages.postman.provide.provide_critical import ProvideCriticalMessage
from bergen.messages.postman.provide.provide_progress import ProvideProgressMessage
from bergen.messages.postman.reserve.reserve_progress import ReserveProgressMessage
from bergen.query import MyType
from bergen.messages.postman import reserve
from bergen.messages.postman.reserve.bounced_reserve import ReserveParams
from bergen.messages.postman.provide.bounced_provide import ProvideParams
from bergen.messages.exception import ExceptionMessage
from bergen.messages.postman.reserve.reserve_critical import ReserveCriticalMessage
from typing import Any
from bergen.schema import AssignationParams, Pod, PodStatus, ProvisionParams
from bergen.registries.arnheim import get_current_arnheim
from bergen.types.model import ArnheimModel
from bergen.extenders.base import BaseExtender
from aiostream import stream
from bergen.console import console
from bergen.messages.postman.reserve import ReserveDoneMessage
from tqdm import tqdm
import textwrap
import logging
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.table import Table
from bergen.monitor.monitor import current_monitor

logger = logging.getLogger(__name__)

class AssignationUIMixin:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ui = None


    def askInputs(self, **kwargs) -> dict:
        widget = self.getWidget(**kwargs) # We have established a ui
        if widget.exec_():
            return widget.parameters
        else:
            return None


    def getWidget(self, **kwargs):
        try:
            from bergen.ui.assignation import AssignationUI
            if not self._ui:
                self._ui = AssignationUI(self.inputs, **kwargs)
            return self._ui
        except ImportError as e:
            raise NotImplementedError("Please install PyQt5 in order to use interactive Widget based parameter query")
            
        




class Reservation:

    def __init__(self, node, loop=None, monitor: Monitor = None, ignore_node_exceptions=False, bounced=None, **params) -> None:
        bergen = get_current_arnheim()
        self._postman = bergen.getPostman()

        self.node = node
        self.params = ReserveParams(**params)
        self.monitor = monitor or current_monitor.get()
        self.ignore_node_exceptions = ignore_node_exceptions

        self.bounced = bounced # with_bounced allows us forward bounced checks
        if self.bounced:
            assert "can_forward_bounce" in bergen.auth.scopes, "In order to use with_bounced forwarding you need to have the can_forward_bounced scope"

        if self.monitor:
            self.monitor.addRow(self.build_panel())
            self.log = lambda level, message: self.table.add_row(level, message)
            self.on_progress = lambda message, level: self.log(f"[magenta]{level}", message) if self.monitor.progress else None
        else:
            self.log = lambda level, message: logger.info(message)
            self.on_progress = False


        self.loop = loop or asyncio.get_event_loop()
        # Status
        self.running = False
        self.reservation = None
        self.critical_error = None
        self.recovering = False #TODO: Implement

        pass
    
    def build_panel(self):
        heading_information = Table.grid(expand=True)
        heading_information.add_column()
        heading_information.add_column(style="green")

        reserving_table = Table(title=f"[bold green]Reserving on ...", show_header=False)
        for key, value in self.params.dict().items():
            reserving_table.add_row(key, str(value))

        heading_information.add_row(self.node.__rich__(), reserving_table)

        self.table = Table()
        self.table.add_column("Level")
        self.table.add_column("Message")

        columns = Table.grid(expand=True)
        columns.add_column()

        columns.add_row(heading_information)
        columns.add_row(self.table)

        return Panel(columns, title="Reservation")

    async def assign(self, *args, **kwargs):
        if self.critical_error is not None:
            
            self.log("[red]ASSIGN",f"Contract is broken and we can not assign. Exiting!")
        try:
            shrinked_args, shrinked_kwargs = await shrinkInputs(self.node, args, kwargs)
            return_message = await self._postman.assign(self.reservation, shrinked_args, shrinked_kwargs=shrinked_kwargs, on_progress=self.on_progress, bounced=self.bounced)
            return await expandOutputs(self.node, return_message.data.returns)

        except NodeException as e:
            self.log("[red]ASSIGN", str(e))
            if not self.ignore_node_exceptions: raise e
        except Exception as e:
            raise e



    def stream(self, *args, **kwargs):
        if self.critical_error is not None:
            self.log("[red]ASSIGN",f"Contract is broken and we can not assign. Exiting!")
        return self._postman.assign_stream(reservation=self.reservation, node=self.node, args=args, kwargs=kwargs, on_progress=self.on_progress, bounced=self.bounced)


    async def contract_worker(self):
        self.running = True
        try:
            async for message in self._postman.reserve_stream(node_id=self.node.id, params_dict=self.params.dict(), with_progress=True, bounced=self.bounced):
                # Before here because Reserve Critical is actually an ExceptionMessage
                #TODO: Undo this

                if isinstance(message, ReserveProgressMessage):
                    self.log(f'[green]{message.data.level.value}', message.data.message)

                if isinstance(message, ProvideProgressMessage):
                    self.log(f'[magenta]{message.data.level.value}', message.data.message)

                if isinstance(message, ReserveCriticalMessage):
                    # Reserve Errors are Errors that happen during the Reservation
                    self.log(f'[red]EXCEPTION', message.data.message)
                    self.critical_error = message

                if isinstance(message, ProvideCriticalMessage):
                    # Reserve Errors are Errors that happen during the Reservation
                    self.log(f'[red]EXCEPTION', message.data.message)
                    self.critical_error = message

                elif isinstance(message, ExceptionMessage):
                    # Porotocol Exceptions are happening on the start
                    self.contract_started.set_exception(message.toException())
                    return

                elif isinstance(message, ReserveDoneMessage):
                    # Once we acquire a reserved resource our contract (the inner part of the context can start)
                    self.contract_started.set_result(message.meta.reference)
        
        except asyncio.CancelledError as e:
            self.log("[green]DONE", "Unreserved Sucessfully")

 
    def cancel_reservation(self, future: Future):
        if future.exception():
            self.log("[red]Exception", str(future.exception()))
            raise future.exception()
        elif future.done():
            return


    async def start(self):
        return await self.__aenter__()

    async def end(self):
        await self.__aexit__()

    async def __aenter__(self):
        self.contract_started = self.loop.create_future()
        self.worker_task = self.loop.create_task(self.contract_worker())
        self.worker_task.add_done_callback(self.cancel_reservation)
        self.reservation = await self.contract_started
        self.log(f"[green]STARTED",f"Established Reservation {self.reservation}")
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self.worker_task.done():
            #await self._postman.unreserve(reservation=self.reservation, on_progress=self.on_progress)
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                self.log("[green]EXIT", "Gently Exiting Reservation")
            except Exception as e:
                self.log(f"[red]CRITICAL", f"Exitigin with {str(e)}")



        

class NodeExtender(AssignationUIMixin, BaseExtender):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        
        bergen = get_current_arnheim()

        self._postman = bergen.getPostman()
        self._loop, self._force_sync = bergen.getLoopAndContext()

    def reserve(self, loop=None, monitor: Monitor = None, ignore_node_exceptions=False, bounced=None, **params) -> Reservation:
        return Reservation(self, loop=loop, monitor=monitor, ignore_node_exceptions=ignore_node_exceptions, bounced=bounced, **params)

    async def stream(self, inputs: dict, params: ReserveParams = None, **kwargs):
        return stream.iterate(self._postman.stream(self, inputs, params, **kwargs))


    async def assign_with_progress(self, inputs, params, **kwargs):
        result = None
        with tqdm(total=100) as pbar:
                async with self.stream_progress(inputs, params, **kwargs) as stream:
                        async for item in stream:
                                result = item
                                if isinstance(result, dict): break
                                
                                progress, message = item.split(":")
                                try: 
                                        pbar.n = int(progress)
                                        pbar.refresh()
                                except:
                                        pass
                                pbar.set_postfix_str(textwrap.shorten(message, width=30, placeholder="..."))
                pbar.n = 100
                pbar.refresh()
                pbar.set_postfix_str("Done")
        return result


    def stream_progress(self,  inputs: dict, params: AssignationParams = None, **kwargs):
        return stream.iterate(self._postman.stream_progress(self, inputs, params, **kwargs)).stream()
    
    def delay(self, inputs: dict, params: AssignationParams = None, **kwargs):
        if self._loop.is_running() and not self._force_sync:
            return self.delay_async(inputs, params, **kwargs)
        else:
            result = self._loop.run_until_complete(self.delay_async(inputs, params, **kwargs))
            return result


    def __call__(self, inputs: dict, params: AssignationParams = None, with_progress = False, **kwargs) -> dict:
        """Call this node (can be run both asynchronously and syncrhounsly)

        Args:
            inputs (dict): The inputs for this Node
            params (AssignationParams, optional): [description]. Defaults to None.

        Returns:
            outputs (dict): The ooutputs of this Node
        """
    
        if self._loop.is_running() and not self._force_sync:
            if with_progress == True:
                return self.assign_with_progress(inputs, params,  with_progress=with_progress, **kwargs)
            return self.assign_async(inputs, params, with_progress=with_progress, **kwargs)

        else:
            if with_progress == True:
                return self._loop.run_until_complete(self.assign_with_progress(inputs, params,  with_progress=with_progress, **kwargs))

            result = self._loop.run_until_complete(self.assign_async(inputs, params,  with_progress=with_progress, **kwargs))
            return result



    def _repr_html_(self):
        string = f"{self.name}</br>"

        for args in self.args:
            string += "Args </br>"
            string += f"Port: {input._repr_html_()} </br>"

        for output in self.outputs:
            string += "Outputs </br>"
            string += f"Port: {output._repr_html_()} </br>"


        return string


    def __rich__(self):
        my_table = Table(title=f"Node: {self.name}", show_header=False)

        my_table.add_row("ID", str(self.id))
        my_table.add_row("Package", self.package)
        my_table.add_row("Interface", self.interface)

        return my_table