from __future__ import annotations

import asyncio
import aiohttp
import json
import logging

from typing import TYPE_CHECKING, Self

_log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .client import Client

class TeamlyWebSocket():
    
    def __init__(self,socket: aiohttp.ClientWebSocketResponse):
        self.socket: aiohttp.ClientWebSocketResponse = socket

    @classmethod
    async def from_client(cls, client: Client) -> Self:
        
        socket = await client.http.ws_connect()
        
        ws = cls(socket)

        return ws

    async def poll_event(self):
        try:
            msg = await self.socket.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.received_message()
            elif msg.type == aiohttp.WSMsgType.BINARY:
                await self.received_message()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                _log.debug("Received error %s", msg)
            elif msg.type in (aiohttp.WSMsgType.CLOSE,aiohttp.WSMsgType.CLOSED,aiohttp.WSMsgType.CLOSING):
                _log.debug("Received %s", msg)
        except:
            print("Could not poll event!!!")

    async def received_message(self):
        pass