

from __future__ import annotations

from .types.blog import Blog as BlogPayload

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .state import ConnectionState

class Blog:

    def __init__(self,*, state: ConnectionState, data: BlogPayload) -> None:
        self.id: str = data['id']
        self.title: str = data['title']
        self.content: str = data['content']
        self.created_at: str = data['createdAt']
        self.created_by: str = data['createdBy']
        self.edited_at: Optional[str] = data.get('editedAt', None)
        self.team_id: str = data['teamId']
        self.hero_image: Optional[str] = data.get('heroImage', None)

    def __repr__(self) -> str:
        return f"<Blog id={self.id} title={self.title} content={self.content}>"
