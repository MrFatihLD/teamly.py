from __future__ import annotations

from typing import Dict, Any, TYPE_CHECKING
from .user import User

if TYPE_CHECKING:
    from .state import ConnectionState

class Message:

    def __init__(self, state: ConnectionState ,data: Dict[str, Any]) -> None:
        self.state: ConnectionState = state
        self.data: Dict[str, Any] = data

    @property
    def author(self) -> User:
        createdby = User(createdby=self.data['createdBy'])
        return createdby
