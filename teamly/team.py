

from __future__ import annotations


from .types.team import Team as TeamPayload, TeamGames as TeamGamesPayload

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .state import ConnectionState


class TeamGames:

    def __init__(self,data: TeamGamesPayload) -> None:
        self.id: int = data['id']
        self.platform: List[str] = data['platform']
        self.region: str = data['region']

    def __repr__(self) -> str:
        return f"<TeamGames id={self.id} platform={self.platform!r}>"

class Team:

    def __init__(self, state: ConnectionState, data: TeamPayload) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]

        self.profile_picture: Optional[str] = data.get("profilePicture")
        self.banner: Optional[str] = data.get("banner")
        self.description: Optional[str] = data.get("description")

        self.is_verified: bool = data.get("isVerified", False)
        self.is_suspended: bool = data.get("isSuspended", False)

        self.created_by: Optional[str] = data.get("createdBy")
        self.default_channel_id: Optional[str] = data.get("defaultChannelId")

        self.games: List[TeamGames] = [TeamGames(g) for g in data.get('games', [])]

        self.is_discoverable: Optional[bool] = data.get("isDiscoverable")
        self.discoverable_invite: Optional[str] = data.get("discoverableInvite")

        self.created_at: Optional[str] = data.get('createdAt')
        self.member_count: Optional[int] = data.get("memberCount")


    def __repr__(self) -> str:
        return f"<Team id={self.id} name={self.name!r} members={self.member_count}>"
