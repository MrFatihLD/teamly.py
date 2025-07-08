






from typing import List, Optional, TypedDict

class TeamGames(TypedDict):
    id: int
    platform: List[str]
    region: str

class Team(TypedDict):
    id: str
    name: str
    profilePicture: str
    banner: str
    description: str
    isVerified: bool
    isSuspended: Optional[bool]
    createdBy: Optional[str]
    defaultChannel: str
    games: List[TeamGames]
    isDiscoverable: Optional[bool]
    discoverableInvite: Optional[str]
    createdAt: Optional[str]
    memberCount: Optional[int]
