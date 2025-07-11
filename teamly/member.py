

from __future__ import annotations


from .user import _UserTag, User
from .types.member import Member as MemberPayload
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .state import ConnectionState


class Member(_UserTag):

    def __init__(self,*, state: ConnectionState, data: MemberPayload) -> None:
        self._state: ConnectionState = state
        self._user: User = User(state=state, data=data)
        self.joined_at: str = data['joinedAt']
        self.roles: List[str] = data.get('roles', [])
        self.teamId: str = data['teamId']

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _UserTag) and other.id == self.id
