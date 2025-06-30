import asyncio

from loguru import logger
from typing import (
    TypeVar,
    Callable,
    Coroutine,
    Any
)

T = TypeVar('T')
Coro = Coroutine[Any,Any, T]
CoroT = TypeVar('CoroT', bound=Callable[..., Coro[Any]])

class Client:

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop = None  # type: ignore

    def run(self, token: str):
        logger.debug('Your token is "{}"', token)

        async def runner():
            logger.debug("starting coroutine")
            async with self:
                await asyncio.sleep(2)

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    def event(self, coro: CoroT,) -> CoroT: #type: ignore
        pass

    async def __aenter__(self):
        logger.debug("Entering context...")
        self.loop = asyncio.get_event_loop()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        logger.debug("Exiting context...")
