from __future__ import annotations

import asyncio
import aiohttp

from typing import Any, Callable, Coroutine, Self, TypeVar
from loguru import logger

from teamly.gateway import TeamlyWebSocket

from .http import HTTPclient
from .gateway import *

T  = TypeVar('T')
Coro = Coroutine[Any, Any, T]
CoroT = TypeVar('CoroT', bound=Callable[..., Coro[Any]])

class Client:

    def __init__(self) -> None:
        self.token: str = None
        self.loop: asyncio.AbstractEventLoop() = None
        self.http: HTTPclient = HTTPclient(loop=self.loop)
        self.ws: TeamlyWebSocket = None

    # run() fonksiyonu içinde async runner() fonksiyonunu tanımlıyoruz.
    # runner() fonksiyonunda, async with self ifadesiyle, self nesnesinin asenkron bağlam yöneticisi metodları (__aenter__ ve __aexit__) çalıştırılır.
    # Bu bağlamda, self.start(token) metodunu await ile bekleyerek çalıştırıyoruz.
    # Bu yapı, kaynakların (bağlantı, oturum vb.) doğru bir şekilde açılmasını ve iş bittikten sonra düzgünce kapanmasını sağlar.
    def run(self, token: str) -> None:

        async def runner():
            logger.debug("runner() started")
            async with self:
                await self.start(token)

        # asyncio.run(runner()) komutu ile runner() adlı asenkron fonksiyon çalıştırılıyor.
        # try-except bloğu sayesinde kullanıcı Ctrl+C ile programı durdurduğunda
        # KeyboardInterrupt hatası yakalanıyor ve program sessizce kapanıyor.
        # Bu, programın ani kesintilerde düzgün şekilde kapanmasını sağlar.
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    # start() fonksiyonu async bir fonksiyondur.
    # Bu fonksiyon içinde self.http.static_login await ile çağrılarak,
    # uygulamanın çalışma süresi boyunca geçerli olacak statik bir aiohttp ClientSession nesnesi oluşturulur.
    async def start(self, token: str) -> None:
        await self.http.static_login(token)
        await self.connect()

    async def connect(self) -> None:
        try:
            coro = TeamlyWebSocket.from_client(self)
            self.ws = await asyncio.wait_for(coro, timeout=60)
            while True:
                await asyncio.sleep(0.5)
                await self.ws.poll_event()
        except Exception as e:
            logger.debug("Error received {}",e)


    # close() fonksiyonu async bir fonksiyondur.
    # Fonksiyon içinde self.http.close() metodu await ile çağrılarak,
    # daha önce açılmış olan aiohttp ClientSession bağlantısı düzgün bir şekilde kapatılır.
    async def close(self) -> None:
        logger.debug("closing ClientSession...")
        await self.http.close()


    async def __aenter__(self) -> Self:
        await self._async_start_hook()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _async_start_hook(self) -> None:
        loop = asyncio.get_running_loop()
        self.loop = loop

    def event(self, coro: CoroT, /) -> CoroT: #For WebSocket events

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')

        setattr(self, coro.__name__, coro)
        logger.debug("\"{coroutine}\" has successfully been registered as an event",coroutine = coro.__name__)
        return coro
