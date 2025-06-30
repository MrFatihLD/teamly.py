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

class _LoopSentinel:
    __slots__ = ()

    def __getattr__(self, attr: str) -> None:
        msg = (
            'loop attribute cannot be accessed in non-async contexts. '
            'Consider using either an asynchronous main function and passing it to asyncio.run or '
            'using asynchronous initialisation hooks such as Client.setup_hook'
        )
        raise AttributeError(msg)

_loop: Any = _LoopSentinel()


class Client:

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop = _loop

    def run(self, token: str) -> None:
        logger.debug('Your token is "{}"', token)

        async def runner():
            logger.debug("starting coroutine")
            async with self:
                await asyncio.sleep(2) #temporaly

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    def event(self, coro: CoroT,) -> CoroT:

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("event registered must be a coroutine function")

        setattr(self, coro.__name__, coro)
        logger.debug("\"{}\" has successfully been registered as an event",coro.__name__)
        return coro

    async def __aenter__(self):
        logger.debug("Entering context...")
        self.loop = asyncio.get_event_loop()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        logger.debug("Exiting context...")
