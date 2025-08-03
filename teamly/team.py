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

from loguru import logger

from teamly import utils

from .category import Category
from .reaction import CustomReaction
from .blog import Blog
from .application import ApplicationSubmission
from .role import Role



from .types.team import TeamPayload, TeamGames as TeamGamesPayload
from typing import TYPE_CHECKING, List, Literal, Optional, Dict, Union, Any

if TYPE_CHECKING:
    from .state import ConnectionState
    from .member import Member

    from .channel import TextChannel, VoiceChannel, AnnouncementChannel, TodoChannel, WatchStreamChannel

    TeamChannels = Union[TextChannel, VoiceChannel, AnnouncementChannel, TodoChannel, WatchStreamChannel]


__all__ = ['Team']


class TeamGames:

    __slots__ = (
        'id',
        'platforms',
        'region'
    )

    def __init__(self, data: TeamGamesPayload) -> None:
        self.id: str = data['id']
        self.platforms: List[str] = data['platforms']
        self.region: str = data['region']


@utils.immuteable
class Team:
    '''Represents a Team

    Attributese
    -----------
    id: :class:`str`
        Unique identifier for the team
    name: :class:`str`
        Name of the team (3 <= name <= 12)
    description: :class:`str`
        A description of the team
    profile_picture: :class:`str <url>`
        URL to the profile picture of the team
    banner: :class:`str <url>`
        URL to the banner image of the team
    is_verified: :class:`bool`
        Indicates whether the team is verified
    is_safe_for_teen: :class:`bool`
        Indicates whether the team is safe for teens
    created_by: :class:`str`
        ID of the user who created the team
    default_channel_id: :class:`str`
        ID of the default channel for the team
    games: :class:`TeamGames`
        List of games associated with the team
    is_discoverable: :class:`bool`
        Indicates whether the team is discoverable
    discoverable_invite: :class:`str <url> | None`
        Invite link for the team if it's discoverable
    created_at: :class:`str <date-time>`
        Timestamp of when the team was created
    member_count: :class:`int`
        Number of members in the team
    '''

    __slots__ = (
        '_state',
        'id',
        'name',
        'profile_picture',
        'banner',
        'description',
        'is_verified',
        'is_safe_for_teen',
        'is_suspended',
        'created_by',
        'default_channel_id',
        'games',
        'is_discoverable',
        'is_tournament',
        'discoverable_invite',
        'created_at',
        'member_count'
    )

    def __init__(self,*, state: ConnectionState, data: TeamPayload) -> None:
        self._state = state
        self.id: str = data['id']
        self.name: str = data['name']
        self.description: Optional[str] = data.get('description')
        self.profile_picture: Optional[str] = data.get('profilePicture')
        self.banner: Optional[str] = data.get('banner')

        self.is_verified: bool = data['isVerified']
        self.is_safe_for_teen: bool = data.get('isSafeForTeen', False)
        self.is_suspended: bool = data['isSuspended']
        self.created_by: str = data['createdBy']
        self.default_channel_id: str = data.get('defaultChannelId')
        self.games: List[TeamGames] = [TeamGames(g) for g in data.get('games')]
        self.is_discoverable: bool = data.get('idDiscoverable', False)
        self.is_tournament: bool = data.get('isTournament', False)
        self.discoverable_invite: Optional[str] = data.get('discoverableInvite')
        self.created_at: str = data['createdAt']
        self.member_count: int = data['memberCount']

    def to_dict(self):
        pass

    #Team

    async def edit(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        banner: Optional[str] = None,
        profilePicture: Optional[str] = None
    ):
        if len(name) > 12:
            raise ValueError("'name' must be smaller or equel then 12 characters")

        if len(description) > 1000:
            raise ValueError("'description' must be smaller or equel then 1000 characters")

        payload = {
            "name": name,
            "description": description,
        }
        if banner:
            payload["banner"] = banner
        if profilePicture:
            payload["profilePicture"] = profilePicture

        await self._state.http.update_team(self.id, payload=payload)


    def info(self) -> str:
        info_list = ["Team:"]

        for slot in self.__slots__[1:]:
            value = getattr(self, slot, None)
            display_value = "N/A" if value is None else value

            parts = slot.split('_')
            display_key = parts[0] + ''.join(word.capitalize() for word in parts[1:])

            if isinstance(display_key, str) and len(display_key) > 30:
                display_value = display_key[:30] + "..."

            info_list.append(f"   {display_key}: {display_value}")

        return "\n".join(info_list)

    #Channel

    async def create_channel(
        self,
        name: str,
        type: Literal['text','voice','watchstream'] = "text",
        *,
        additionalData: Optional[Dict[str,str]] = None
    ):
        payload = {
            "name": name,
            "type": type,
        }

        if (type == "watchstream") and (additionalData is None):
            raise ValueError("if you create watchstream channel. You need a additionalData")

        if additionalData:
            if additionalData["streamChannel"] is None:
                raise ValueError("You need to add a URL for the streamChannel")
            if additionalData["streamPlatform"] not in ('twitch', 'kick'):
                raise ValueError("Pls enter a valid streamPlatform")

            payload["additionalData"] = additionalData

        return await self._state.http.create_channel(teamId=self.id, payload=payload)

    async def delete_channel(self, channelId: str):
        await self._state.http.delete_channel(teamId=self.id, channelId=channelId)

    async def update_channel(
        self,
        channelId: str,
        name: str,
        *,
        additionalData: Optional[Dict[str,str]] = None
    ):
        channel = self._state.cache.get_channel(teamId=self.id, channelId=channelId)
        payload = {}
        if channel:
            payload["name"] = name
            if additionalData:
                if additionalData["streamChannel"] is None:
                    raise ValueError("You need to add a URL for the streamChannel")
                if additionalData["streamPlatform"] not in ('twitch', 'kick'):
                    raise ValueError("Pls enter a valid streamPlatform")

                payload["additionalData"] = additionalData

            await self._state.http.update_channel(teamId=self.id, channelId=channel.id, payload=payload)

    ##burasi yapilacak
    async def update_channel_permissions(self, channelId: str, roleId: str, payload: Dict[str,int]):
        channel = self._state.cache.get_channel(teamId=self.id, channelId=channelId)
        if channel:
            await self._state.http.update_channel_permissions(teamId=self.id, channelId=channelId, roleId=roleId,payload=payload)


    async def duplicate_channel(self, channelId: str):
        await self._state.http.duplicate_channel(teamId=self.id, channelId=channelId)

    async def update_channel_priority(self, channels: List[TeamChannels]):
        payload = {"channels": [channel.to_dict() for channel in channels]}
        await self._state.http.update_channel_priorities(teamId=self.id, payload=payload)

    def get_channels(self):
        return self._state.cache.get_channels(teamId=self.id)

    def get_channel(self, channelId: str):
        return self._state.cache.get_channel(teamId=self.id, channelId=channelId)

    #Member

    def get_members(self) -> Dict[str, Member]:
        return self._state.cache.get_members(teamId=self.id)

    def get_member(self, userId: str):
        return self._state.cache.get_member(teamId=self.id, userId=userId)




    async def ban(self, userId: str, reason: str):
        return await self._state.http.ban(teamId=self.id, userId=userId, reason=reason)

    async def unban(self, userId: str):
        return await self._state.http.unban(teamId=self.id, userId=userId)

    async def get_ban_list(self, teamId: str, limit: int = 10):
        if limit > 1000:
            raise ValueError("Limit is to big! max value is 1000")
        return await self._state.http.get_banned_users(teamId=teamId, limit=limit)


    async def kick(self, userId: str):
        try:
            await self._state.http.kick_member(teamId=self.id, userId=userId)
        except Exception:
            return

        self._state.cache.delete_member(teamId=self.id,memberId=userId)

    #Role

    async def add_role(self, role: Role):
        return await self._state.http.create_role(teamId=self.id, payload=role.to_dict())

    async def update_role(self,roleId: str, role: Role):
        return await self._state.http.update_role(teamId=self.id,roleId=roleId, payload=role)

    async def update_role_priorities(self, roles: List[str]):
        payload = {"roles": roles}
        return await self._state.http.update_role_priorities(teamId=self.id, payload=payload)

    async def delete_role(self, roleId: str):
        await self._state.http.delete_role(teamId=self.id, roleId=roleId)

    async def clone_role(self, roleId: str):
        await self._state.http.clone_role(teamId=self.id, roleId=roleId)

    async def get_roles(self):
        return await self._state.http.get_roles(teamId=self.id)

    async def assigne_role(self, userId: str, roleId: str):
        return await self._state.http.add_role_to_member(teamId=self.id, userId=userId, roleId=roleId)

    async def unassigne_role(self, userId: str, roleId: str):
        return await self._state.http.remove_role_from_member(teamId=self.id, userId=userId, roleId=roleId)

    #Application

    async def get_application_submission(self):
        application = await self._state.http.get_application_submissions(teamId=self.id)
        return ApplicationSubmission(state=self._state,team=self,data=application)

    async def update_application_status(self, applicationId: str, status: Literal['accepted', 'rejected']):
        return await self._state.http.update_application_status(teamId=self.id, applicationId=applicationId, status=status)

    async def update_team_application_status(self, enable: bool):
        return await self._state.http.update_team_application_status(teamId=self.id, enable=enable)

    async def update_team_application_questions(self, payload: Dict[str,List[Dict[str,str]]]):
        return await self._state.http.update_team_application_questions(teamId=self.id, payload=payload)

    async def get_application(self, applicationId: str):
        return await self._state.http.get_application_by_id(teamId=self.id, applicationId=applicationId)


    #Reactions

    async def get_team_custom_reactions(self):
        reactions = await self._state.http.get_team_custom_reactions(teamId=self.id)
        return [CustomReaction(state=self._state, data=r) for r in reactions['reactions']]

    async def create_new_custom_reaction(self, name: str, emoji: Any):
        await self._state.http.create_new_custom_reaction_for_team(teamId=self.id,name=name, emoji=emoji)

    async def update_team_custom_reaction(self,reactionId: str, name: str):
        await self._state.http.update_custom_reaction(teamId=self.id, reactionId=reactionId, name=name)

    async def delete_team_custom_reaction(self, reactionId: str):
        await self._state.http.delete_custom_reaction(teamId=self.id, reactionId=reactionId)


    #Blog

    async def get_blog_posts(self) -> List[Blog]:
        blogs = await self._state.http.get_blog_posts(teamId=self.id)
        return [Blog(state=self._state, team=self, data=data) for data in blogs]

    async def create_blog_post(self, title: str, content: str, heroImage: Optional[str] = None):
        payload = {
            "title": title,
            "content": content,
            "heroImage": heroImage
        }
        return await self._state.http.create_blog_post(teamId=self.id, payload=payload)

    async def delete_blog_post(self, blogId: str):
        return await self._state.http.delete_blog_post(teamId=self.id, blogId=blogId)


    #category

    async def get_category(self, categoryId: str) -> Category | None:
        data = await self._state.http.get_channels(teamId=self.id)
        for category in data["categories"]:
            if category['id'] == categoryId:
                return Category(state=self._state, team=self, data=category)
        logger.error("Category not found.")
        return None

    async def create_category(self, name: str):
        return await self._state.http.create_category(teamId=self.id,name=name)

    async def update_category(self, categoryId: str, name: str):
        return await self._state.http.update_category(teamId=self.id, categoryId=categoryId, name=name)

    async def update_category_permissions(self, categoryId: str, roleId: str, **kwargs: Optional[bool]):
        CATEGORY = (
            'view_channels',
            'manage_channels'
        )
        allow = 0
        deny = 0

        for key in kwargs:
            if key not in CATEGORY:
                raise ValueError(f"'{key}' is not a valid permission for the category")

        for i, name in enumerate(CATEGORY):
            bit = kwargs.get(name)
            if bit is True:
                allow |= (1 << i)
            if bit is False:
                deny |= (1 << i)

        return await self._state.http.update_category_role_permission(
            teamId=self.id,
            categoryId=categoryId,
            roleId=roleId,
            allow=allow,
            deny=deny
       )

    async def delete_category(self, categoryId: str):
        return await self._state.http.delete_category(teamId=self.id, categoryId=categoryId)

    async def delete_channel_from_category(self, categoryId: str, channelId: str):
        return await self._state.http.delete_channel_from_category(teamId=self.id, categoryId=categoryId, channelId=channelId)

    async def set_channel_priority_of_category(self, categoryId: str, channelIds: List[str]):
        payload = {"channels": channelIds}
        return await self._state.http.set_channel_priority_of_category(teamId=self.id, categoryId=categoryId, payload=payload)

    async def set_category_priority(self, categoryIds: List[str]):
        payload = {"categories": categoryIds}
        return await self._state.http.set_team_category_priority(teamId=self.id, payload=payload)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"<Team id={self.id} name={self.name} description={self.description}"
            f" isVerified={self.is_verified} isDiscoverable={self.is_discoverable}>"
        )
