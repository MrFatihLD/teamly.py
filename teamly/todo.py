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

from typing import Optional, TYPE_CHECKING
from .types.todo import TodoItem as TodoItemPayload

if TYPE_CHECKING:
    from .state import ConnectionState

class TodoItem:

    def __init__(self,state: ConnectionState ,data: TodoItemPayload) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: str = data['content']
        self.created_by: str = data['createdBy']
        self.edited_by: Optional[str] = data.get('editedBy', None)
        self.edited_at: Optional[str] = data.get('editedAt', None)
        self.completed: bool = data['completed']
        self.completed_by: Optional[str] = data.get('completedBy', None)
        self.completed_at: Optional[str] = data.get('completedAt', None)
        self.created_at: str = data['createdAt']

    def to_dict(self):
        return {
            "id": self.id,
            "channelId": self.channel_id,
            "type": self.type,
            "content": self.content,
            "createdBy": self.created_by,
            "editedBy": self.edited_by,
            "editedAt": self.edited_at,
            "completed": self.completed,
            "completedBy": self.completed_by,
            "completedAt": self.completed_at,
            "createdAt": self.created_at
        }

    async def delete(self):
        await self._state.http.delete_todo_item(channelId=self.channel_id, todoId=self.id)

    async def update(self, content: str, completed: bool = False):
        return await self._state.http.update_todo_item(channelId=self.channel_id, todoId=self.id, content=content, completed=completed)

    def __repr__(self) -> str:
        return f"<TodoItem id={self.id} content={self.content} completed={self.completed} channelId={self.channel_id}>"
