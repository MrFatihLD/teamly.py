

from __future__ import annotations

from datetime import datetime, timezone

from .user import _UserTag, User
from .types.member import Member as MemberPayload
from typing import TYPE_CHECKING, Dict, List, Mapping, Any, cast

if TYPE_CHECKING:
    from .state import ConnectionState
    from .user import UserPayload


class Member(User,_UserTag):

    def __init__(self,*, state: ConnectionState, data: MemberPayload) -> None:
        self._state: ConnectionState = state
        self._update(data)

    def _update(self, data: Mapping):
        super()._update(data)
        self.joined_at: str = data['joinedAt']
        self.roles: List[str] = data.get('roles', [])
        self.teamId: str = data['teamId']

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _UserTag) and other.id == self.id

    @classmethod
    def _new_member(cls,state: ConnectionState, data: UserPayload, teamId: str):

        member_data: Dict[str,Any] = dict(data)
        member_data['joinedAt'] = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
        member_data['roles'] = []
        member_data[teamId] = teamId

        return cls(state=state, data=cast(MemberPayload, member_data))

    def __repr__(self) -> str:
        return f"<Member username={self._user.username} joined_at={self.joined_at} roles={self.roles} teamId={self.teamId}>"
