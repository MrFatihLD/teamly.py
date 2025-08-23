'''
MIT License

Copyright (c) 2025 Fatih Kuloglu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

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

    async def edit(self, name: str):
        await self._state.http.update_category(teamId=self.team.id, categoryId=self.id, name=name)

    async def update_permissions(self, roleId: str, allow: int, deny: int):
        await self._state.http.update_category_role_permission(teamId=self.team.id, categoryId=self.id, roleId=roleId, allow=allow, deny=deny)

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

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} teamId={self.team.id}>"
