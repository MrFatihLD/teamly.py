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

import asyncio
import aiohttp
import json

from asyncio.timeouts import Optional




from .utils import MISSING
from typing import Any, Dict
from urllib.parse import quote
from loguru import logger

class Route:
    '''
        Represents an API route with a method and path, used to build full request URLs
        for the Teamly API.

        Example:
            Route("GET", "/channels/{channel_id}", channel_id="1234")
            → https://api.teamly.one/api/v1/channels/1234

        Attributes:
            BASE_URL (str): The base URL for all API requests.
            method (str): The HTTP method (e.g., "GET", "POST").
            path (str): The API path, possibly containing placeholders.
            url (str): The fully constructed request URL.
    '''

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

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self._session: aiohttp.ClientSession = MISSING
        self.token = None
        self.loop: asyncio.AbstractEventLoop = loop

    async def static_login(self, token: str):
        logger.debug("static logging...")

        self.token = token
        self._session = aiohttp.ClientSession()

    async def close(self):
        logger.debug("closing client session...")
        await self._session.close()

    async def ws_connect(self) -> aiohttp.ClientWebSocketResponse:
        logger.debug("creating ws connect...")

        kwargs = {
            "timeout": 30,
            "max_msg_size": 0,
            "headers": {
                "Authorization": f'Bot {self.token}'
            }
        }

        return await self._session.ws_connect(url="wss://api.teamly.one/api/v1/ws", **kwargs)

    async def request(self, route: Route, **kwargs) -> Any:
        method = route.method
        url = route.url

        #creating headers
        headers = {}

        if self.token is not None:
            headers["Authorization"] = f'Bot {self.token}'

        if 'json' in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs['data'] = json.dumps(kwargs.pop('json'))

        kwargs["headers"] = headers

        try:
            logger.debug("making request...")
            return await self._session.request(method, url, **kwargs)
        except Exception as e:
            logger.error("Exception error: {}",e)


    #Core Resources

    #Channels
    async def get_channels(self, teamId: str):
        return await self.request(Route("GET","/teams/{teamId}/channels", teamId=teamId))

    async def create_channel(self, teamId: str, payload: Dict[str,Any]):
        r = Route("PUT", "/teams/{teamId}/channels", teamId=teamId)
        return await self.request(r,json=payload)

    async def delete_channel(self, teamId: str, channelId: str):
        r = Route("DELETE","/teams/{teamId}/channels/{channelId}", teamId=teamId, channelId=channelId)
        return await self.request(r)

    async def duplicate_channel(self, teamId: str, channelId: str):
        r = Route("POST","/teams/{teamId}/channels/{channelId}/clone", teamId=teamId, channelId=channelId)
        return await self.request(r)

    async def update_channel_priorities(self, teamId: str, channelId: str, payload: Dict[str, Any]):
        r = Route("PUT","/teams/{teamId}/channelspriority", teamId=teamId)
        return await self.request(r,json=payload)

    async def get_channel_by_Id(self, teamId: str, channelId: str):
        r = Route("GET","/teams/{teamId}/channels/{channelId}", teamId=teamId, channelId=channelId)
        return await self.request(r)




    async def update_channel(self, teamId: str, channelId: str, payload: Dict[str, Any]):
        r = Route("PATCH","/teams/{teamId}/channels/{channelId}", teamId=teamId, channelId=channelId)
        return await self.request(r, json=payload)

    async def update_channel_permissions(self, teamId: str, channelId: str, roleId: str, allow: int, deny: int):
        payload = {"allow": allow, "deny": deny}
        r = Route("POST","/teams/{teamId}/channels/{channelId}/permissions/role/{roleId}", teamId=teamId, channelId=channelId, roleId=roleId)
        return await self.request(r,json=payload)



    #Message
    async def create_message(self, channelId: str, payload: Dict[str,Any]):
        r = Route("POST","/channels/{channelId}/messages", channelId=channelId)
        return await self.request(r,json=payload)

    async def delete_message(self, channelId: str, messageId: str):
        r = Route("DELETE","/channels/{channelId}/messages/{messageId}",messageId=messageId, channelId=channelId)
        return await self.request(r)

    async def get_channel_messages(self, channelId: str, offset: Optional[str], limit: str = 15):
        r = Route("GET","/channels/{channelId}/messages" + f"?offset={offset}&limit={limit}", channelId=channelId)
        return await self.request(r)

    async def update_channel_message(self, channelId: str, messageId: str, payload: Dict[str, Any]):
        r = Route("PATCH","/channels/{channelId}/messages/{messageId}", channelId=channelId, messageId=messageId)
        return await self.request(r,json=payload)

    async def react_to_message(self, channelId: str, messageId: str, emojiId: str):
        r = Route("POST","/channels/{channelId}/messages/{messageId}/reactions/{emojiId}", channelId=channelId, messageId=messageId, emojiId=emojiId)
        return await self.request(r)

    async def delete_reaction_from_message(self, channelId: str, messageId: str, emojiId: str):
        r = Route("DELETE","/channels/{channelId}/messages/{messageId}/reactions/{emojiId}", channelId=channelId, messageId=messageId, emojiId=emojiId)
        return await self.request(r)

    async def get_channel_by_id(self, channelId: str, messageId: str):
        r = Route("GET","/channels/{channelId}/messages/{messageId}", channelId=channelId, messageId=messageId)
        return await self.request(r)
