'''
MIT License

Copyright (c) 2025 Fatih Kuloglu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from __future__ import annotations

import asyncio
import threading
import aiohttp
import json
import time

from typing import TYPE_CHECKING, Any, Optional
from loguru import logger

if TYPE_CHECKING:
    from .client import Client


class GatewayRatelimiter:
    def __init__(self, count: int = 110, per: float = 60.0) -> None:
        # The default is 110 to give room for at least 10 heartbeats per minute
        self.max: int = count
        self.remaining: int = count
        self.window: float = 0.0
        self.per: float = per
        self.lock: asyncio.Lock = asyncio.Lock()

    def is_ratelimited(self) -> bool:
        current = time.time()
        if current > self.window + self.per:
            return False
        return self.remaining == 0

    def get_delay(self) -> float:
        current = time.time()

        if current > self.window + self.per:
            self.remaining = self.max

        if self.remaining == self.max:
            self.window = current

        if self.remaining == 0:
            return self.per - (current - self.window)

        self.remaining -= 1
        return 0.0

    async def block(self) -> None:
        async with self.lock:
            delta = self.get_delay()
            if delta:
                logger.warning('WebSocket is ratelimited, waiting {} seconds',delta)
                await asyncio.sleep(delta)


class KeepAliveHandler(threading.Thread):

    def __init__(self, ws, loop: asyncio.AbstractEventLoop, interval: Optional[float] = None):
            super().__init__()
            self.ws: TeamlyWebSocket = ws
            self.loop: asyncio.AbstractEventLoop = loop
            self.interval: Optional[float] = interval
            self._stop_event: threading.Event = threading.Event()
            self._last_send: float = time.perf_counter()
            self._last_ack: float = time.perf_counter()

    def run(self):
        while not self._stop_event.wait(self.interval):
            if time.perf_counter() - self._last_ack > self.interval * 2: #type: ignore
                print("[ThreadedHeartbeat] ACK alınamadı, bağlantı ölü olabilir.")
                continue

            self._last_send = time.perf_counter()

            payload = {
                "t": "HEARTBEAT",
                "d": {}
            }

            coro = self.ws.socket.send_json(payload)
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
            try:
                future.result(timeout=10)
            except Exception as e:
                print("[ThreadedHeartbeat] send error:", e)

    def stop(self):
        self._stop_event.set()

    def ack(self):
        self._last_ack = time.perf_counter()

class TeamlyWebSocket:

    def __init__(self, socket: aiohttp.ClientWebSocketResponse,*, loop: asyncio.AbstractEventLoop) -> None: #type: ignore
        self.socket: aiohttp.ClientWebSocketResponse = socket
        self._keep_alive: Optional[KeepAliveHandler] = None

    @classmethod
    async def from_client(cls, client: Client):
        socket = await client.http.ws_connect()
        ws = cls(socket, loop=client.loop)

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
