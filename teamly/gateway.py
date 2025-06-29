from __future__ import annotations

import asyncio
import aiohttp
import json

from typing import Any

from loguru import logger

class TeamlyWebSocket:

    def __init__(self, socket: aiohttp.ClientWebSocketResponse,*, loop: asyncio.AbstractEventLoop) -> None:
        self.socket: aiohttp.ClientWebSocketResponse = socket
        self.loop: asyncio.AbstractEventLoop = loop


    @classmethod
    async def from_client(cls, client: Client):
        socket = await client.http.ws_connect()
        ws = cls(socket, loop=client.loop)

        ws.token = client.http.token

        logger.debug("Created WebSocket connection.")

        return ws


    async def poll_event(self) -> None:
        try:
            msg = await self.socket.receive()
            if msg.type is aiohttp.WSMsgType.TEXT:
                await self.received_message(msg.data)
            elif msg.type is aiohttp.WSMsgType.BINARY:
                await self.received_message(msg.data)
            elif msg.type is aiohttp.WSMsgType.ERROR:
                logger.debug("Received error {}", msg)
            elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING):
                logger.debug("Received {}", msg)
        except:
            logger.error("\"event_poll\" not executed")

    async def received_message(self, msg: Any) -> None:
        if type(msg) is bytes:
            msg = msg.decode("utf-8")

        if msg is None:
            return

        msg = json.loads(msg)

        event = msg.get('t')
        if event:
            pass

        print(json.dumps(msg,indent=4,ensure_ascii=False))
