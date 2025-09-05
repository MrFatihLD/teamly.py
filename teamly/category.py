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
from typing import TYPE_CHECKING, Any, Dict, List, Optional


if TYPE_CHECKING:
    from .state import ConnectionState


class Category:

    def __init__(self, state: ConnectionState, data: CategoryPayload) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.team_id: str = data['teamId']
        self.name: str = data['name']
        self.created_by: str = data['createdBy']
        self.priority: Optional[int] = data.get('priority')
        self.permissions: Dict[str, Any] = data['permissions']
        self.created_at: str = data['createdAt']
        self.edited_at: Optional[str] = data.get('editedAt')

    async def update(self, name: str):
        await self._state.http.update_category(teamId=self.team_id, categoryId=self.id, name=name)

    async def update_role_permissions(self, roleId: str, /, allow: int, deny: int):
        await self._state.http.update_category_role_permission(teamId=self.team_id, categoryId=self.id, roleId=roleId, allow=allow, deny=deny)

    async def delete(self):
        await self._state.http.delete_category(teamId=self.team_id, categoryId=self.id)

    async def set_channel_priority(self, channels: List[str]):
        payload = {"channels": channels}
        await self._state.http.set_channel_priority_of_category(teamId=self.team_id, categoryId=self.id, payload=payload)



    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} teamId={self.team_id}>"
