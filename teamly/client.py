import asyncio
import aiohttp
import logging


from .http import HTTPClient
from .gateway import *

from typing import Coroutine, Callable, TypeVar, Any

_log = logging.getLogger(__name__)

T = TypeVar('T') # 'T' Herhangi bit tipi temsil eder
Coro = Coroutine[Any,Any,T] #asenkron bir fonksiyonu temsil eder
CoroT = TypeVar('CoroT', bound = Callable[..., Coro[Any]]) # Coroutine döndüren herhangi bir fonksiyon tipi

class Client:

    def __init__(self):
        self.http = HTTPClient()
        self.ws: TeamlyWebSocket = None

    def run(self, token: str):

        async def runner():
            _log.debug("started \"runner()\"") #Debug
            async with self:
                await self.start(token)

        self.setup_logging()

        _log.debug("running \"asyncio.run(runner())\"") #Debug

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass        

    async def start(self, token: str):
        _log.debug("Started \"start()\"...") #Debug
        await self.http.static_login(token)
        await self.connect()

    async def connect(self):
        try:
            coro = TeamlyWebSocket.from_client(self)
            self.ws = await asyncio.wait_for(coro,timeout=60)
            await self.ws.poll_event()
        except:
            print("didnt work")

    async def close(self):
        await self.http.close()

    def setup_logging(self): #temp
        _log.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        _log.addHandler(console_handler)





    async def __aenter__(self):
        pass

    async def __aexit__(
            self, 
            exc_type, 
            exc_val, 
            exc_tb
    ):
        _log.debug("closing HTTP client...")
        await self.http.close()