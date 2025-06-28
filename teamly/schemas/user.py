from ast import Not
from typing import TypedDict, Optional, NotRequired, List

class Badge(TypedDict):
    id: str
    name: str
    icon: str

class UserStatus(TypedDict):
    content: Optional[str]
    emojiId: Optional[str]

class UserRPC(TypedDict):
    type: Optional[str]
    name: Optional[str]
    id: Optional[str]
    startedAt: Optional[str]

class User(TypedDict):
    id: str
    username: str
    subdomain: str
    profilePicture: NotRequired[str]
    banner: NotRequired[str]
    bot: bool
    presence: int
    flags: str
    badges: List[Badge]
    userStatus: NotRequired[UserStatus]
    userRPC: NotRequired[UserRPC]
    connections: List
    createdAt: str
    system: bool
