from __future__ import annotations

import asyncio
import aiohttp
import json



from typing import TYPE_CHECKING, Self

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
                if msg.data is not None:
                    data = json.loads(msg.data)
                    print(json.dumps(data,indent=4))
                    await self.socket.close()
        except:
            print("Could not poll event!!!")