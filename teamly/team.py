

from __future__ import annotations




from .channel import TextChannel, VoiceChannel
from .member import Member

from .types.team import TeamPayload, TeamGames as TeamGamesPayload
from typing import TYPE_CHECKING, Dict, List, Optional, Union

if TYPE_CHECKING:
    from .state import ConnectionState

_TeamChannelTypes = Union[TextChannel,VoiceChannel]

class TeamGames:

    def __init__(self, data: TeamGamesPayload) -> None:
        self.id: str = data['id']
        self.platforms: List[str] = data['platforms']
        self.region: str = data['region']

class Team:

    def __init__(self,*, state: ConnectionState, data: TeamPayload) -> None:
        self._state = state
        self._channels: Dict[str, _TeamChannelTypes] = {}
        self._members: Dict[str, Member] = {}
        self._update(data)

    def _update(self, data: TeamPayload):
        self.id: str = data['id']
        self.name: str = data['name']
        self.profile_picture: Optional[str] = data.get('profilePicture')
        self.banner: Optional[str] = data.get('banner')
        self.description: Optional[str] = data.get('description')

        self.is_verified: bool = data['isVerified']
        self.is_suspended: bool = data['isSuspended']
        self.created_by: str = data['createdBy']
        self.default_channel_id: str = data.get('defaultChannelId')
        self.games: List[TeamGames] = [TeamGames(g) for g in data.get('games')]
        self.is_discoverable: bool = data.get('idDiscoverable', False)
        self.discoverable_invite: Optional[str] = data.get('discoverableInvite')
        self.created_at: str = data['createdAt']
        self.member_count: int = data['memberCount']

    async def update_team(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        banner: Optional[str] = None,
        profilePicture: Optional[str] = None
    ):
        if len(name) > 12:
            raise ValueError("\'name\' must be smaller or equel then 12 characters")

        if len(description) > 1000:
            raise ValueError("\'description\' must be smaller or equel then 1000 characters")

        all_args = locals()

        payload = {
            key: value
            for key, value in all_args.items()
            if key in {"name","description","banner","profilePicture"} and value is not None
        }

        return self._state.http.update_team(self.id, payload=payload)


    def __repr__(self) -> str:
        return (
            f"<Team id={self.id} name={self.name} description={self.description}"
            f" isVerified={self.is_verified} isDiscoverable={self.is_discoverable}>"
        )
