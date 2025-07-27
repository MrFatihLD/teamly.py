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





from .types.team import TeamPayload, TeamGames as TeamGamesPayload
from typing import TYPE_CHECKING, List, Optional, Dict

if TYPE_CHECKING:
    from .state import ConnectionState
    from .role import Role
    from .member import Member


__all__ = ['Team']

def immuteable(cls):
    original_setattr = cls.__setattr__

    def new_setattr(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"'{name}' is immuteable and cannot be reassigned.")
        original_setattr(self, name, value)

    cls.__setattr__ = new_setattr
    return cls

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


@immuteable
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

    Methods
    --------
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
        self.profile_picture: Optional[str] = data.get('profilePicture')
        self.banner: Optional[str] = data.get('banner')
        self.description: Optional[str] = data.get('description')

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
            k:v
            for k,v in locals().items()
            if v is not None
        }

        await self._state.http.update_team(self.id, payload=payload)


    def info(self) -> str:
        info_list = ["Team:"]

        for slot in self.__slots__:
            value = getattr(self, slot, None)
            display_value = "N/A" if value is None else value

            parts = slot.split('_')
            display_key = parts[0] + ''.join(word.capitalize() for word in parts)

            if isinstance(display_key, str) and len(display_key) > 30:
                display_value = display_key[:30] + "..."

            info_list.append(f"\t{display_key}: {display_value}")

        return "\n".join(info_list)


    #Member

    def fetch_members(self) -> Dict[str, Member]:
        return self._state.cache.get_members(teamId=self.id)

    def get_member(self, userId: str):
        return self._state.cache.get_member(teamId=self.id, userId=userId)




    async def ban(self, userId: str, reason: str):
        return await self._state.http.ban(teamId=self.id, userId=userId, reason=reason)

    async def unban(self, userId: str):
        return await self._state.http.unban(teamId=self.id, userId=userId)

    async def get_banned_users(self, teamId: str, limit: int = 10):
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

    async def remove_role(self, roleId: str):
        return await self._state.http.delete_role(teamId=self.id, roleId=roleId)

    async def list_roles(self):
        return await self._state.http.get_roles(teamId=self.id)

    async def assigne_role(self, userId: str, roleId: str):
        return await self._state.http.add_role_to_member(teamId=self.id, userId=userId, roleId=roleId)

    async def unassigne_role(self, userId: str, roleId: str):
        return await self._state.http.remove_role_from_member(teamId=self.id, userId=userId, roleId=roleId)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"<Team id={self.id} name={self.name} description={self.description}"
            f" isVerified={self.is_verified} isDiscoverable={self.is_discoverable}>"
        )
