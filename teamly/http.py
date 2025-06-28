import aiohttp
import json

from aiohttp.web import Response
from aiohttp.web_request import Request

from .schemas import user

from typing import ClassVar, Any, Dict, List, Literal, Optional
from loguru import logger
from urllib.parse import quote

class Route:
    """
    --
    API istekleri için URL ve HTTP methodunu tanımlar.

    Özellikler:
        BASE_URL (str): API'nin temel URL'si.

    Parametreler:
        method (str): HTTP methodu (GET, POST, DELETE, PATCH, vb.).
        path (str): API uç noktası (endpoint) için yol. İçinde formatlanabilir parametreler olabilir.
        **params: path içinde yerleştirilecek değişkenler veya ayrıca kullanılacak ID'ler.

    Örnek:
        Route("GET", "/teams/{team_id}/channels/{channel_id}", team_id="abc", channel_id="xyz")

        Bu örnek şu URL'yi oluşturur:
        https://api.teamly.one/api/v1/teams/abc/channels/xyz
    """

    BASE_URL: ClassVar = "https://api.teamly.one/api/v1"

    def __init__(self, method: str, path: str, **params: Any) -> None:
        self.method = method    # HTTP methodunu kaydet
        self.path = path    # Endpoint yolunu kaydet

        # Parametreleri path'in içine yerleştirerek tam URL'yi oluştur
        url = self.BASE_URL + self.path
        if params:
            url = url.format_map({k: quote(v, safe='') if isinstance(v, str) else v for k, v in params.items()})
        self.url = url

        # Bazı özel ID'leri ayrıca tut (isteğe bağlı)
        self.channelId = params.get("channelId")
        self.teamId = params.get("teamId")
        self.webhookId = params.get("webhookId")
        self.webhookToken = params.get("webhookToken")

class HTTPclient:

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession = None
        self.token: str = None

    async def ws_connect(self) -> aiohttp.ClientWebSocketResponse:
        kwargs = {
            "timeout": 30,
            "autoclose": False,
            "headers": {
                "Authorization": f"Bot {self.token}"
            }
        }

        logger.debug("connecting to WebSocket...")
        return await self._session.ws_connect("wss://api.teamly.one/api/v1/ws", **kwargs)

    async def static_login(self, token: str):
        logger.debug("setting ClientSession...")
        self._session = aiohttp.ClientSession()
        self.token = token

    async def request(self, route: Route, **kwargs):
        method = route.method
        url = route.url

        headers = {
            "Authorization": f'Bot {self.token}'
        }

        if 'json' in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop('json'))

        kwargs["headers"] = headers

        try:
            async with self._session.request(method, url, **kwargs) as response:
                logger.debug(f"request sended: {method} {url} {kwargs}")

                data = await response.json()

                print(json.dumps(data,indent=4,ensure_ascii=False))

                return data
        except:
            logger.debug("request could not be sended!!!")

    async def close(self):
        await self._session.close()
        logger.debug("ClientSession closed")


    #Request fonksiyonlari
    #Channels
    async def update_team_channel(self,*, teamId: str, channelId: str, **fields: Any):
        r = Route("PATCH","/teams/{teamId}/channels/{channelId}",teamId=teamId, channelId=channelId)
        return await self.request(r,json=fields)

    async def update_channel_role_permissions(self,*, teamId: str, channelId: str, roleId: str, **fields: Any):
        r = Route("POST","/teams/{teamId}/channels/{channelId}/permissions/role/{roleId}",teamId=teamId,channelId=channelId,roleId=roleId)
        return await self.request(r,json=fields)

    async def get_team_channel(self, teamId: str):
        return await self.request(Route("GET","/teams/{teamId}/channels"))

    async def create_team_channel(self, teamId: str, **fields):
        r = Route("PUT","/teams/{teamId}/channels")
        return await self.request(r, json=fields)

    async def delete_team_channel(self, teamId: str, channelId: str):
        return await self.request(Route("DELETE","/teams/{teamId}/channels/{channelId}", teamId=teamId, channelId=channelId))

    async def duplicate_team_channel(self, teamId: str, channelId: str):
        return await self.request(Route("POST","/teams/{teamId}/channels/{channelId}/clone", teamId=teamId, channelId=channelId))

    async def update_channels_priorities(self, teamId: str, **fields):
        r = Route("PUT","/teams/{teamId}/channelspriority", teamId=teamId)
        return await self.request(r, json=fields)

    async def get_channel(self, teamId: str, channelId: str):
        return await self.request(Route("GET","/teams/{teamId}/channels/{channelId}", teamId=teamId, channelId=channelId))


    #Messages
    async def create_channel_message(self, channelId: str, **fields):
        r = Route("POST","/channels/{channelId}/messages", channelId=channelId)
        return await self.request(r, json=fields)

    async def delete_channel_message(self, channelId: str, messageId: str):
        return await self.request(Route("DELETE","/channels/{channelId}/messages/{messageId}", channelId=channelId, messageId=messageId))

    async def get_channel_messages(self, channelId: str, **fields):
        r = Route("GET","/channels/{channelId}/messages", channelId=channelId)
        return await self.request(r, json=fields)

    async def update_channel_message(self, channelId: str, messageId: str, **fields):
        r = Route("PATCH","/channels/{channelId}/messages/{messageId}", channelId=channelId, messageId=messageId)
        return await self.request(r, json=fields)

    async def react_message(self, channelId: str, messageId: str, emojiId: str):
        return await self.request(Route("POST","/channels/{channelId}/messages/{messageId}/reactions/{emojiId}", channelId=channelId, messageId=messageId, emojiId=emojiId))

    async def delete_reaction_from_message(self, channelId: str, messageId: str, emojiId: str):
        return await self.request(Route("DELETE","/channels/{channelId}/messages/{messageId}/reactions/{emojiId}", channelId=channelId, messageId=messageId, emojiId=emojiId))

    async def get_channel_message(self, channelId: str, messageId: str):
        return await self.request(Route("GET","/channels/{channelId}/messages/{messageId}", channelId=channelId, messageId=messageId))



    #Teams

    #Members
    async def add_role_to_member(self, teamId: str, userId: str, roleId: str):
        r = Route("POST","/teams/{teamId}/members/{userId}/roles/{roleId}", teamId=teamId, userId=userId, roleId=roleId)
        return await self.request(r)

    async def remove_role_from_member(self, teamId: str, userId: str, roleId: str):
        r = Route("DELETE","/teams/{teamId}/members/{userId}/roles/{roleId}", teamId=teamId, userId=userId, roleId=roleId)
        return await self.request(r)

    async def kick(self, teamId: str, userId: str):
        r = Route("DELETE","/teams/{teamId}/members/{userId}", teamId=teamId, userId=userId)
        return await self.request(r)

    async def get_member(self, teamId: str, userId: str):
        r = Route("GET","/teams/{teamId}/members/{userId}", teamId=teamId, userId=userId)
        return await self.request(r)


    #Bans
    async def get_banned_users(self, teamId: str, **fields):
        r = Route("GET","/teams/{teamId}/bans", teamId=teamId)
        return await self.request(r, json=fields)

    async def unban_user(self, teamId: str, userId: str):
        r = Route("DELETE","/teams/{teamId}/members/{userId}/ban", teamId=teamId, userId=userId)
        return await self.request(r)

    async def ban(self, teamId: str, userId: str, reason: Optional[str]):
        r = Route("POST","/teams/{teamId}/members/{userId}/ban", teamId=teamId, userId=userId)
        json = {"reason": reason}
        return await self.request(r, json=json)

    async def get_team(self, teamId: str):
        return await self.request(Route("GET","/teams/{teamId}/details", teamId=teamId))

    async def update_team(self, teamId: str, **fields):
        r = Route("POST","/teams/{teamId}", teamId=teamId)
        return await self.request(r, json=fields)




    #Roles
    async def create_role(self, teamId: str, **fields):
        r = Route("POST","/teams/{teamId}/roles", teamId=teamId)
        return await self.request(r, json=fields)

    async def get_role(self, teamId: str):
        return await self.request(Route("GET","/teams/{teamId}/roles", teamId=teamId))

    async def delete_role(self, teamId: str, roleId: str):
        r = Route("DELETE","/teams/{teamId}/roles/{roleId}", teamId=teamId, roleId=roleId)
        return await self.request(r)

    async def clone_role(self, teamId: str, roleId: str):
        r = Route("POST","/teams/{teamId}/roles/{roleId}/clone", teamId=teamId, roleId=roleId)
        return await self.request(r)

    async def update_role_priorities(self, teamId: str, role_ids: List[str]):
        r = Route("PATCH","/teams/{teamId}/roles-priority", teamId=teamId)
        return await self.request(r, json=role_ids)

    async def update_role(self, teamId: str, roleId: str, **fields):
        r = Route("POST","/teams/{teamId}/roles/{roleId}", teamId=teamId, roleId=roleId)
        return await self.request(r,json=fields)




    #Users
    async def get_user(self, userId: str):
        return await self.request(Route("GET","/users/{userId}",userId=userId))

    async def get_loggedIn_user(self):
        return await self.request(Route("GET","/me"))




    #Todos
    async def get_todo_items(self, channelId: str):
        return await self.request(Route("GET","/channels/{channelId}/todo/list", channelId=channelId))

    async def create_todo_item(self, channelId: str, content: str):
        payload = {"content": content}
        return await self.request(Route("POST","/channels/{channelId}/todo/item", channelId=channelId), json=payload)

    async def delete_todo_item(self, channelId: str, todoId: str):
        r = Route("DELETE","/channels/{channelId}/todo/item/{todoId}", channelId=channelId, todoId=todoId)
        return await self.request(r)

    async def clone_todo_item(self, channelId: str, todoId: str):
        r = Route("POST","/channels/{channelId}/todo/item/{todoId}/clone", channelId=channelId, todoId=todoId)
        return await self.request(r)

    async def update_todo_item(self, channelId: str, todoId: str, payload: Dict):
        r = Route("PUT","/channels/{channelId}/todo/item/{todoId}", channelId=channelId, todoId=todoId)
        return await self.request(r, json=payload)




    #Direct Messages
    async def create_direct_message(self, payload: Dict):
        return await self.request(Route("POST","/me/chats"), json=payload)



    #Applications
    async def get_application_submissions(self, teamId: str):
        return await self.request(Route("GET","/teams/{teamId}/applications", teamId=teamId))

    async def update_application_status(self, teamId: str, applicationId: str, status: Literal["accepted","rejected"]):
        payload = {"status": status}
        r = Route("POST","/teams/{teamId}/applications/{applicationId}", teamId=teamId, applicationId=applicationId)
        return await self.request(r, json=payload)

    async def update_team_application_status(self, teamId: str, enable: bool):
        payload = {"enable": enable}
        r = Route("POST","/teams/{teamId}/applications/status", teamId=teamId)
        return await self.request(r, json=payload)

    async def update_team_application_questions(self, teamId: str, payload: Dict[str,Any]):
        r = Route("PATCH","/teams/{teamId}/applications", teamId=teamId)
        return await self.request(r, json=payload)

    async def get_application(self, teamId: str, applicationId: str):
        return await self.request(Route("GET","/teams/{teamId}/applications/{applicationId}", teamId=teamId, applicationId=applicationId))





    #Reaction
    async def get_team_custom_reactions(self, teamId: str):
        return await self.request(Route("GET","/teams/{teamId}/reactions", teamId=teamId))

    async def create_team_custom_reaction(self, teamId: str): #Not Ready for execute
        r = Route("POST","/teams/{teamId}/reactions", teamId=teamId)
        return await self.request(r)

    async def update_custom_reaction(self, teamId: str, reactionId: str, name: str):
        payload = {"name": name}
        r = Route("PUT","/teams/{teamId}/reactions/{reactionId}", teamId=teamId, reactionId=reactionId)
        return await self.request(r, json=payload)

    async def delete_custom_reaction(self, teamId: str, reactionId: str):
        r = Route("DELETE","/teams/{teamId}/reactions/{reactionId}", teamId=teamId, reactionId=reactionId)
        return await self.request(r)




    #Attachments
    async def upload_attachment(self): #Not Ready for execute
        r = Route("POST","/upload")
        return await self.request(r)




    #Voice
    async def get_credentials_for_join_voice_channel(self, teamId: str, channelId: str): #Not Ready for execute
        r = Route("GET","/teams/{teamId}/channels/{channelId}/join", teamId=teamId, channelId=channelId)
        return await self.request(r)

    async def update_own_voice_metadata(self, teamId: str, channelId: str, isMuted: bool, isDeafened: bool):
        payload = {"isMuted": isMuted, "isDeafened": isDeafened}
        r = Route("POST","/teams/{teamId}/channels/{channelId}/metadata", teamId=teamId, channelId=channelId)
        return await self.request(r, json=payload)

    async def leave_voice_channel(self, teamId: str, channelId: str):
        r = Route("GET","/teams/{teamId}/channels/{channelId}/leave", teamId=teamId, channelId=channelId)
        return await self.request(r)




    #Webhook
    async def create_message_with_webhook(self, webhookId: str, webhookToken: str, payload: Dict[str, Any]):
        r = Route("POST","/webhooks/{webhookId}/{webhookToken}", webhookId=webhookId, webhookToken=webhookToken)
        return await self.request(r, json=payload)

    async def webhook_for_github(self, webhookId: str, webhookToken: str):
        r = Route("POST","/webhooks/{webhookId}/{webhookToken}/github", webhookId=webhookId, webhookToken=webhookToken)
        return await self.request(r)




    #Blog
    async def get_blog_posts(self, teamId: str):
        r = Route("GET","/teams/{teamId}/blogs", teamId=teamId)
        return await self.request(r)

    async def create_blog_post(self, teamId: str, payload: Dict[str,Any]):
        r = Route("POST","/teams/{teamId}/blogs", teamId=teamId)
        return await self.request(r,json=payload)

    async def delete_blog_post(self, teamId: str, blogId: str):
        r = Route("DELETE","/teams/{teamId}/blogs/{blogId}", teamId=teamId, blogId=blogId)
        return await self.request(r)





    #Category
    async def create_category(self, teamId: str, name: str):
        payload = {"name": name}
        return await self.request(Route("POST","/teams/{teamId}/categories", teamId=teamId), json=payload)

    async def update_category(self, teamId: str, categoryId: str, name: str):
        payload = {"name": name}
        r = Route("PUT","/teams/{teamId}/categories/{categoryId}", teamId=teamId, categoryId=categoryId)
        return await self.request(r, json=payload)

    async def update_category_role_permissions(self, teamId: str, categoryId: str, roleId: str, allow: int, deny: int):
        payload = {"allow": allow, "deny": deny}
        r = Route("POST","/teams/{teamId}/categories/{categoryId}/permissions/role/{roleId}", teamId=teamId, categoryId=categoryId, roleId=roleId)
        return await self.request(r,json=payload)

    async def delete_category(self, teamId: str, categoryId: str):
        r = Route("DELETE","/teams/{teamId}/categories/{categoryId}", teamId=teamId, categoryId=categoryId)
        return await self.request(r)

    async def add_channel_to_category(self, teamId: str, categoryId: str, channelId: str):
        r = Route("POST","/teams/{teamId}/categories/{categoryId}/channels/{channelId}", teamId=teamId, categoryId=categoryId, channelId=channelId)
        return await self.request(r)

    async def delete_channel_from_category(self, teamId: str, categoryId: str, channelId: str):
        r = Route("DELETE","/teams/{teamId}/categories/{categoryId}/channels/{channelId}", teamId=teamId, categoryId=categoryId, channelId=channelId)
        return await self.request(r)

    async def set_channel_priority_of_category(self, teamId: str, categoryId: str, channels: List[str]):
        payload = {"channels": channels}
        r = Route("POST","/teams/{teamId}/categories/{categoryId}/channels-priority", teamId=teamId, categoryId=categoryId)
        return await self.request(r, json=payload)

    async def set_team_category_priority(self, teamId: str, categories: List[str]):
        payload = {"categories": categories}
        r = Route("POST","/teams/{teamId}/categories-priority", teamId=teamId)
        return await self.request(r, json=payload)

    async def get_announcments(self, channelId: str):
        r = Route("GET","/channels/{channelId}/announcements",channelId=channelId)
        return await self.request(r)

    async def create_annoucement(self, channelId: str, payload: Dict[str,Any]):
        r = Route("POST","/channels/{channelId}/announcements", channelId=channelId)
        return await self.request(r, json=payload)

    async def delete_annoucement(self, channelId: str, announcementId: str):
        r = Route("DELETE","/channels/{channelId}/announcements/{announcementId}",channelId=channelId, announcementId=announcementId)
        return await self.request(r)
