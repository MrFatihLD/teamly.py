
from __future__ import annotations


from .types.category import Category as CategoryPayload
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from .state import ConnectionState
    from .team import Team


class Category:

    __slots__ = (
        '_state',
        'team',
        'id',
        'name',
        '_created_by',
        'priority',
        '_permissions',
        'created_at',
        'edited_at'
    )

    def __init__(
        self,
        state: ConnectionState,
        team: Team,
        data: CategoryPayload
    ) -> None:
        self._state: ConnectionState = state
        self.team: Team = team

        self.id: str = data['id']
        self.name: str = data['name']
        self._created_by: str = data['createdBy']
        self.priority: str = data.get('priority')
        self._permissions: str = data.get('permissions', {})
        self.created_at: str = data["createdAt"]
        self.edited_at: str = data.get("editedAt")

    @property
    def createdBy(self):
        try:
            return self._state.cache.get_member(teamId=self.team.id, userId=self._created_by)
        except AttributeError:
            return self._created_by

    @property
    def permissions(self) -> List[Dict[str,Dict]] | None:
        list = []
        if self._permissions["role"]:
            for p in self._permissions["role"]:
                list.append(
                    {
                        p['roleId']:{
                            "allow": p['allow'],
                            "deny": p['deny']
                        }
                    }
                )
            return list
        else:
            return None

    def to_dict(self):
        payload = {
            "id": self.id,
            "teamId": self.team.id,
            "name": self.name,
            "createdBy": self._created_by,
            "priority": self.priority,
            "permissions": self._permissions,
            "createdAt": self.created_at,
            "editedAt": self.edited_at
        }
        return payload
