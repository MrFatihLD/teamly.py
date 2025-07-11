

from __future__ import annotations

from typing import List, Optional, TypedDict

from teamly.abc import StatusLiteral

class UserRPC(TypedDict):
    type: Optional[str]
    name: Optional[str]
    id: Optional[str]
    startedAt: Optional[str]

class UserStatus(TypedDict):
    content: Optional[str]
    emojiId: Optional[str]

class Badges(TypedDict):
    id: str
    name: str
    icon: str

class User(TypedDict):
    id: str
    username: str
    subdomain: str
    profilePicture: Optional[str]
    banner: Optional[str]
    bot: bool
    presence: StatusLiteral
    flags: str
    badges: List[Badges]
    userStatus: Optional[UserRPC]
    userRPC: Optional[UserRPC]
    connections: List[str]
    createdAt: str
    system: bool
    verified: bool
    disabled: bool
