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

from teamly.channel import _channel_factory

from .member import Member

from .types.team import Team as TeamPayload
from typing import TYPE_CHECKING, Dict, List, Literal, Optional

if TYPE_CHECKING:
    from .state import ConnectionState


class Team:

    def __init__(self, state: ConnectionState, data: TeamPayload) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.name: str = data['name']
        self.profile_picture: Optional[str] = data.get('profilePicture')
        self.banner: Optional[str] = data.get('banner')
        self.description: Optional[str] = data.get('description')
        self.is_verified: bool = data['isVerified']
        self.is_suspended: bool = data.get('isSuspended')
        self.created_by: str = data['createdBy']
        self.default_channel_id: Optional[str] = data.get('defaultChannelId')
        self.games: Optional[List[Dict]] = data.get('games', [])
        self.is_discoverable: bool = data['isDiscoverable']
        self.discoverable_invite: Optional[str] = data.get('discoverableInvite')
        self.created_at: str = data['createdAt']
        self.member_count: int = data['memberCount']

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "profilePicture": self.profile_picture,
            "banner": self.banner,
            "description": self.description,
            "isVerified": self.is_verified,
            "isSuspended": self.is_suspended,
            "createdBy": self.created_by,
            "defaultChannelId": self.default_channel_id,
            "games": self.games,
            "isDiscoverable": self.is_discoverable,
            "discoverableInvite": self.discoverable_invite,
            "createdAt": self.created_at,
            "memberCount": self.member_count
        }

    async def edit(
        self,
        name: str,
        description: str = None,
        /,
        banner: str = None,
        profilePicture: str = None
    ):
        payload = {
            "name": name,
            "description": description,
            "banner": banner,
            "profilePicture": profilePicture
        }
        await self._state.http.update_team(teamId=self.id, payload=payload)

    #Team

    async def add_role_to_member(self, userId: str, roleId: str):
        await self._state.http.add_role_to_member(teamId=self.id, userId=userId, roleId=roleId)

    async def remove_role_from_member(self, userId: str, roleId: str):
        await self._state.http.remove_role_from_member(teamId=self.id, userId=userId, roleId=roleId)

    async def get_member(self, userId: str):
        member = await self._state.http.get_member(teamId=self.id, userId=userId)['member']
        return Member(state=self._state, data=member)

    async def get_banned_users(self, limit: int = 10):
        return await self._state.http.get_banned_users(teamId=self.id, limit=limit)

    async def unban(self, userId: str):
        await self._state.http.unban(teamId=self.id, userId=userId)

    async def ban(self, userId: str,/, reason: str = None):
        await self._state.http.ban(teamId=self.id, userId=userId, reason=reason)

    async def kick(self, userId: str):
        await self._state.http.kick_member(teamId=self.id, userId=userId)

    #Channel

    async def get_channels(self):
        return await self._state.http.get_channels(teamId=self.id)

    async def get_channelJ(self, channelId: str):
        return await self._state.http.get_channel_by_Id(teamId=self.id, channelId=channelId)

    async def create_channel(
        self,
        name: str,
        type: Literal['text', 'voice', 'watchstream', 'todo', 'announcement'] = "text",
        /,
        additionalData: Dict[str, str] = None
    ):
        payload = {
            "name": name,
            "type": type,
            "addtionalData": additionalData
        }
        await self._state.http.create_channel(teamId=self.id, payload=payload)

    async def delete_channel(self, channelId: str):
        await self._state.http.delete_channel(teamId=self.id, channelId=channelId)

    async def update_channel(self, channelId: str, name: str, /, additionalData: Dict[str, str] = None):
        payload = {"name": name, "additionalData": additionalData}
        await self._state.http.update_channel(teamId=self.id, channelId=channelId, payload=payload)

    async def update_channel_permissions(self, channelId: str, roleId, /, allow: int, deny: int):
        payload = {"allow": allow, "deny": deny}
        await self._state.http.update_channel_permissions(teamId=self.id, channelId=channelId, roleId=roleId, payload=payload)

    async def duplicate_channel(self, channelId: str):
        await self._state.http.duplicate_channel(teamId=self.id, channelId=channelId)


    #Roles



    def __repr__(self) -> str:
        return f"<Team id={self.id} name={self.name!r} isVerified={self.is_verified} memberCount={self.member_count}>"
