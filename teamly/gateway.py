from __future__ import annotations

import aiohttp
import json

from typing import TYPE_CHECKING
from aiohttp.web_exceptions import Any
from loguru import logger

if TYPE_CHECKING:
    from .client import Client

class TeamlyWebSocket:

    def __init__(self, socket: aiohttp.ClientWebSocketResponse) -> None:
        self.socket: aiohttp.ClientWebSocketResponse = socket

    @classmethod
    async def from_client(cls, client: Client):
        socket = await client.http.ws_connect()
        ws = cls(socket)

        await ws.poll_event()

        return ws

    async def poll_event(self):
        '''
            Continuously polls the WebSocket connection for incoming messages.

            Depending on the message type (text, binary, error, or close),
            it delegates the message to the appropriate handler or logs it.

            This function is meant to be run in an event loop (e.g., inside a task).
        '''

        try:
            msg = await self.socket.receive()
            if msg.type is aiohttp.WSMsgType.TEXT:
                await self.received_message(msg.data)
            elif msg.type is aiohttp.WSMsgType.BINARY:
                await self.received_message(msg.data)
            elif msg.type is aiohttp.WSMsgType.ERROR:
                logger.error("Received: ", msg)
            elif msg.type in (
                aiohttp.WSMsgType.CLOSE,
                aiohttp.WSMsgType.CLOSED,
                aiohttp.WSMsgType.CLOSING
            ):
                logger.debug("Received: {}",msg)
        except Exception as e:
            logger.error("Exception error {}",e)

    async def received_message(self, msg: Any):
        if type(msg) is bytes:
            msg = msg.decode('utf-8')

        if msg is None:
            return

        msg = json.loads(msg)

        print(json.dumps(msg,indent=4,ensure_ascii=False))
