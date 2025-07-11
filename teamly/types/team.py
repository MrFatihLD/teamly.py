

from __future__ import annotations


from typing import List, Optional, TypedDict

class TeamGames(TypedDict):
    id: str
    platforms: List[str]
    region: str

class TeamPayload(TypedDict):
    id: str
    name: str
    profilePicture: Optional[str]
    banner: Optional[str]
    description: Optional[str]
    isVerified: bool
    isSuspended: Optional[bool]
    createdBy: str
    defaultChannelId: Optional[str]
    games: List[TeamGames]
    idDiscoverable: Optional[bool]
    discoverableInvite: Optional[str]
    createdAt: str
    memberCount: int
