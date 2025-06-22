import asyncio
import aiohttp
import json
import logging

from typing import Optional, ClassVar, Any

from .gateway import TeamlyWebSocket
from urllib.parse import quote


_log = logging.getLogger(__name__)

class Route:
    BASE_URL: ClassVar[str] = "https://api.teamly.one/api/v1"

    def __init__(self, method: str, path: str,**params: Any):
        self.method = method
        self.path = path

        url = self.BASE_URL + self.path
        if params:
            url = url.format_map({k: quote(v, safe='') if isinstance(v, str) else v for k, v in params.items()})
        self.url = url

        self.channel_id = params.get("channel_id")
        self.team_id = params.get("team_id")
        self.webhook_id = params.get("webhook_id")
        self.webhook_token = params.get("webhook_id")

    

class HTTPClient:
     
    def __init__(
            self,
            connector: Optional[aiohttp.BaseConnector] = None
        ):
        self.__session: aiohttp.ClientSession = None
        self.connector: aiohttp.BaseConnector = connector or None #Missing

        self.token: str = None


    #Websocket ile baglanmayi saglayacak fonksiyon
    async def ws_connect(self) -> aiohttp.ClientWebSocketResponse:
        kwargs = {
            "timeout": 30,
            "autoclose": False,
            "headers": {
                "Authorization": f"Bot {self.token}" #Buraya botun tokeni gelecek
            }
        }
        return await self.__session.ws_connect('wss://api.teamly.one/api/v1/ws',**kwargs)

    async def static_login(self, token: str): #ClientSessionu baslatacak fonksiyon
        if self.connector is None:
            self.connector = aiohttp.TCPConnector(limit=0)

        self.__session = aiohttp.ClientSession(
            connector=self.connector,
            ws_response_class=TeamlyWebSocket
        )

        self.token = token

    async def close(self):
        await self.__session.close()

    async def request(self, route: Route, **kwargs):
        method = route.method
        url = route.url

        headers = {
            "Authorization": f"Bot {self.token}"
        }

        if 'json' in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop('json'))

        kwargs['headers'] = headers

        response: Optional[aiohttp.ClientResponse] = None

        try:
            async with self.__session.request(method, url, **kwargs) as response:
                _log.debug("request sended: %s %s %s",method, url, **kwargs)

                data = await response.json()

                print(json.dumps(data,indent=4))
        except:
            _log.debug("could not send a request!!!") #Debug

    async def test_request(self):
        await self.request(Route("GET","/me"))

