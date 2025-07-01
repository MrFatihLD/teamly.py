import aiohttp
import json

from .utils import MISSING
from typing import Any
from urllib.parse import quote

class Route:
    BASE_URL = "https://api.teamly.one/api/v1"

    def __init__(self, method:str, path: str, **params: Any) -> None:
        self.method = method
        self.path = path

        url = self.BASE_URL + self.path
        if params:
            url = url.format_map({
                k: quote(v, safe='') if isinstance(v, str) else v
                for k, v in params.items()
            })
        self.url: str = url

class HTTPClient:

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession = MISSING
        self.token = None

    async def static_login(self, token: str):
        self.token = token
        self._session = aiohttp.ClientSession()


    async def ws_connect(self):
        kwargs = {
            "timeout": 30,
            "max_msg_size": 0,
            "headers": {
                "Authorization": f'Bot {self.token}'
            }
        }

        return await self._session.ws_connect(url="wss://api.teamly.one/api/v1/ws", **kwargs)

    async def request(self, route: Route, **kwargs) -> aiohttp.ClientResponse:
        method = route.method
        url = route.url

        #creating headers
        headers = {}

        if self.token is not None:
            headers["Authorization"] = f'Bot {self.token}'

        if 'json' in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs['data'] = json.dumps(kwargs.pop('json'))

        return await self._session.request(method, url, **kwargs)
