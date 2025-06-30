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
        """
            Starts the asynchronous event loop with the given token.

            This method initializes and runs the main coroutine (`runner`),
            which currently contains a temporary sleep call for testing purposes.
            In a production environment, this would be replaced with actual logic.

            Args:
                token (str): The token used to authenticate or start the process.
        """

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
        """
            The `event` decorator registers a coroutine function as an event handler.

            This method checks whether the given function is a coroutine. If it is,
            it sets the coroutine as an attribute of the instance, allowing it to be
            called or referenced later as an event. Otherwise, it raises a TypeError.

            Args:
                coro (CoroT): A coroutine function to be registered as an event.

            Returns:
                CoroT: The same coroutine function, unmodified.

            Raises:
                TypeError: If the provided function is not a coroutine.
        """

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("event registered must be a coroutine function")

        setattr(self, coro.__name__, coro)
        logger.debug("\"{}\" has successfully been registered as an event",coro.__name__)
        return coro

    async def _run_event(
        self,
        coro: Callable[...,Coroutine[Any,Any,Any]],
        event_name: str,
        *arg,
        **kwargs
    ) -> None:
        try:
            await coro(*arg, **kwargs)
        except Exception as e:
            logger.error("The event could not run {}",e)

    async def _schedul_event(
        self,
        coro: Callable[..., Coroutine[Any,Any,Any]],
        event_name: str,
        *arg,
        **kwargs
    ):
        wrapper = self._run_event(coro, event_name, *arg, **kwargs)
        #scheduls event
        return self.loop.create_task(wrapper, name=f"Teamly.py: {event_name}")

    async def __aenter__(self):
        logger.debug("Entering context...")
        self.loop = asyncio.get_event_loop()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        logger.debug("Exiting context...")
