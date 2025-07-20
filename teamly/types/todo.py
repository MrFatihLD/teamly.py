

from __future__ import annotations

from typing import Optional, TypedDict


class TodoItem(TypedDict):
    id: str
    channelId: str
    type: str
    content: str
    createdBy: str
    editedBy: Optional[str]
    editedAt: Optional[str]
    completed: bool
    completedBy: Optional[str]
    completedAt: Optional[str]
    createdAt: str
