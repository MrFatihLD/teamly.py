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
from typing import TYPE_CHECKING, Dict, Optional, List

from .todo import TodoItem
from .enums import ChannelType
from .types.channel import (
    TextChannel as TextChannelPayload,
    TodoChannel as TodoChannelPayload
)

if TYPE_CHECKING:
    from .state import ConnectionState





class TextChannel:
    """
    Attributes
    ---
    id: :class:`str`
    type: :class:`str`
    team_id: :class:`str`
    name: :class:`str`
    description: :class:`Optional[str]`
    created_by: :class:`str`
    created_at: :class:`str`
    parent_id: :class:`Optional[str]`
    priority: :class:`int`
    permissions: :class:`Optional[dict]`
    rate_limit_per_user: :class:`int`
    additional_data: :class:`Optional[dict]`
    """


    def __init__(self, state: ConnectionState, data: TextChannelPayload) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']
        self.description: Optional[str] = data.get('description')
        self.created_by: str = data['createdBy']
        self.created_at: str = data['createdAt']
        self.parent_id: Optional[str] = data.get('parentId')
        self.priority: int = data['priority']
        self.permissions: Optional[Dict] = data.get('permissions', {})
        self.rate_limit_per_user: int = data['rateLimitPerUser']
        self.additional_data: Optional[Dict] = data.get('additionalData', {})

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "teamId": self.team_id,
            "name": self.name,
            "description": self.description,
            "createdBy": self.created_by,
            "createdAt": self.created_at,
            "parentId": self.parent_id,
            "priority": self.priority,
            "permissions": self.permissions,
            "rateLimitPerUser": self.rate_limit_per_user,
            "additionalData": self.additional_data
        }

    async def edit(self, name: str, description: str = None):
        payload = {"name": name, "description": description}
        await self._state.http.update_channel(
            teamId=self.team_id,
            channelId=self.id,
            payload=payload
        )

    async def update_role(self, roleId: str, /, allow: int, deny: int):
        payload = {"allow": allow, "deny": deny}
        await self._state.http.update_channel_permissions(
            teamId=self.team_id,
            channelId=self.id,
            roleId=roleId,
            payload=payload
        )

    async def delete(self):
        await self._state.http.delete_channel(
            teamId=self.team_id,
            channelId=self.id
        )

    def __repr__(self) -> str:
        return f"<TextChannel id={self.id} name={self.name} type={self.type} teamId={self.team_id}>"



class TodoChannel:

    def __init__(self, state: ConnectionState, data: TodoChannelPayload) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']
        self.description: Optional[str] = data.get('description')
        self.created_by: str = data['createdBy']
        self.created_at: str = data['createdAt']
        self.parent_id: Optional[str] = data.get('parentId')
        self.priority: int = data['priority']
        self.permissions: Optional[Dict] = data.get('permissions', {})
        self.additional_data: Optional[Dict] = data.get('additionalData', {})

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "teamId": self.team_id,
            "name": self.name,
            "description": self.description,
            "createdBy": self.created_by,
            "createdAt": self.created_at,
            "parentId": self.parent_id,
            "priority": self.priority,
            "permissions": self.permissions,
            "additionalData": self.additional_data
        }

    async def edit(self, name: str, description: str = None):
        payload = {"name": name, "description": description}
        await self._state.http.update_channel(
            teamId=self.team_id,
            channelId=self.id,
            payload=payload
        )

    async def update_role(self, roleId: str, /, allow: int, deny: int):
        payload = {"allow": allow, "deny": deny}
        await self._state.http.update_channel_permissions(
            teamId=self.team_id,
            channelId=self.id,
            roleId=roleId,
            payload=payload
        )

    async def delete(self):
        await self._state.http.delete_channel(
            teamId=self.team_id,
            channelId=self.id
        )

    #special TodoChannel functions

    async def get_todo_items(self) -> List[TodoItem]:
        todos = await self._state.http.get_todo_items(channelId=self.id)['todos']
        return [TodoItem(state=self._state, data=todo) for todo in todos]

    async def create_todo_item(self, content: str):
        await self._state.http.create_todo_item(channelId=self.id, content=content)

    async def delete_todo_item(self, todoId: str):
        await self._state.http.delete_todo_item(channelId=self.id, todoId=todoId)

    async def clone_todo_item(self, todoId: str):
        await self._state.http.clone_todo_item(channelId=self.id, todoId=todoId)

    async def update_todo_item(self, todoId: str, content: str, completed: bool = False):
        await self._state.http.update_todo_item(channelId=self.id, todoId=todoId, content=content, completed=completed)



    def __repr__(self) -> str:
        return f"<TodoChannel id={self.id} name={self.name} type={self.type} teamId={self.team_id}>"


class WatchStream:
    pass


def _channel_factory(type: str):
    if ChannelType.TEXT == type:
        return TextChannel
    elif ChannelType.TODO == type:
        return TodoChannel
    elif ChannelType.WATCHSTREAM == type:
        return WatchStream
    else:
        return None
