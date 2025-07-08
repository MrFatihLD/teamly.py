





from typing import Optional, TypedDict


class TodoItem(TypedDict):
    id: str
    channelId: str
    type: str
    createdBy: str
    editedBy: Optional[str]
    editedAt: Optional[str]
    completed: bool
    completedBy: Optional[str]
    completedAt: Optional[str]
    createdAt: str
