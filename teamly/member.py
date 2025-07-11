

from __future__ import annotations


from .types.member import Member as MemberPayload
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ConnectionState


class Member:

    def __init__(self,*, state: ConnectionState, data: MemberPayload) -> None:
        self._state: ConnectionState = state
