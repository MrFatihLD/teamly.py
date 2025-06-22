import asyncio
import aiohttp

from .client import Client

class TeamlyWebSocket():
    
    def __init__(self, socket: aiohttp.ClientWebSocketResponse):
        self.socket: aiohttp.ClientWebSocketResponse = socket

    @classmethod
    async def from_client(
        cls,
        client: Client
        ):

        socket = client.http.ws_connect()
        #ws = cls(socket)