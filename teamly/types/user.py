


from typing import TypedDict, Optional, List

class UserBadges(TypedDict):
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
    profilePicture: Optional[str]
    banner: Optional[str]
    bot: bool
    presence: int
    flags: str
    badges: UserBadges
    userStatus: Optional[UserStatus]
    userRPC: Optional[UserRPC]
    connections: List[str]
    createdAt: str
    system: bool
