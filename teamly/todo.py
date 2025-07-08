



from typing import Optional
from .types.todo import TodoItem


class Todo:

    def __init__(self, data: TodoItem) -> None:
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: str = data['createdBy']

        self.created_by: str = data['createdBy']

        self.edited_by: Optional[str] = data.get('editedBy', None)
        self.edited_at: Optional[str] = data.get('editedAt', None)

        self.completed: bool = data['completed']
        self.completed_by: Optional[str] = data.get('completedBy', None)
        self.completed_at: Optional[str] = data.get('completedAt', None)

        self.created_at: str = data['createdAt']
