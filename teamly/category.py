
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ConnectionState
    from .team import Team


class Category:

    def __init__(
        self,
        state: ConnectionState,
        team: Team,
        data: dict
    ) -> None:
        self._state: ConnectionState = state
        self.team: Team = team

        self.id: str = data['id']
        self.name: str = data['name']
