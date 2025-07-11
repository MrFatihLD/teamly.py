

from __future__ import annotations

from .user import User
from typing import List, TypedDict


class Member(User, TypedDict):
    joinedAt: str
    roles: List[str]
    teamId: str
