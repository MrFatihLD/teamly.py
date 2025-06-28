from __future__ import annotations

import asyncio
import aiohttp
import json
import logging
import time

from typing import TYPE_CHECKING, Self, Any

_log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .client import Client

class GatewayRatelimiter:

    def __init__(self):
        self.window: float = 0.0
        self.period: float = 60.0
        self.remaining: int = 0
        self.max: int = 20000

    def delay(self) -> float:
        curent = time.time()

        if curent > self.window + self.period:
            self.remaining = self.max

        if self.remaining == self.max:
            self.window = curent

        if self.remaining == 0:
            return self.period - (self.window - curent)

        self.remaining -= 1
        return 0.0
    
    async def block(self):
        delta = self.delay()
        if delta:
            _log.debug("Blocked rate for %.2f", delta)
            await asyncio.sleep(delta)


class TeamlyWebSocket():
    
    def __init__(self,socket: aiohttp.ClientWebSocketResponse):
        self.socket: aiohttp.ClientWebSocketResponse = socket
        self._ratelimit: GatewayRatelimiter = GatewayRatelimiter()

    @classmethod
    async def from_client(cls, client: Client) -> Self:
        
        socket = await client.http.ws_connect()
        
        ws = cls(socket)

        return ws

    async def poll_event(self):
        try:
            msg = await self.socket.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.received_message(msg.data)
            elif msg.type == aiohttp.WSMsgType.BINARY:
                await self.received_message(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                _log.debug("Received error %s", msg)
            elif msg.type in (aiohttp.WSMsgType.CLOSE,aiohttp.WSMsgType.CLOSED,aiohttp.WSMsgType.CLOSING):
                _log.debug("Received %s", msg)
        except:
            print("Could not poll event!!!")

    async def received_message(self, msg, /):
        if type(msg) is bytes:
            msg = msg.decode('utf-8')

        if msg is None:
            return

        msg = json.loads(msg)

        print(json.dumps(msg,indent=4,ensure_ascii=False))

        event_t = msg['t']
        data = msg['d']

    
    
    async def close(self):
        await self.socket.close()

    async def send(self, data: str, /):
        await self._ratelimit.block()
        await self.socket.send_str(data)
