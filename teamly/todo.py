

from __future__ import annotations

from .types.todo import TodoItem as TodoItemPayload
from typing import TYPE_CHECKING, Mapping, Optional


if TYPE_CHECKING:
    from teamly.state import ConnectionState

class TodoItem:

    def __init__(self, state: ConnectionState, data: TodoItemPayload) -> None:
        self._state: ConnectionState = state
        self.from_dict(data)

    def from_dict(self, data: Mapping):
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: str = data['content']

        self.created_by: str = data['createdBy']
        self.edited_by: Optional[str] = data.get('editedBy')
        self.edited_at: Optional[str] = data.get('editedAt')
        self.completed: bool = data['completed']
        self.completed_by: Optional[str] = data.get('completedBy')
        self.completed_at: Optional[str] = data.get('completedAt')
        self.createdAt: str = data['createdAt']

    def __repr__(self) -> str:
        return f"<TodoItem id={self.id} channelId={self.channel_id} type={self.type} content={self.content}>"
