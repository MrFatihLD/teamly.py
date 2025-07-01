import aiohttp

from .utils import MISSING


class HTTPClient:

    def __init__(self) -> None:
        self._socket: aiohttp.ClientSession = MISSING

    async def static_login(self):
        self._socket = aiohttp.ClientSession()
