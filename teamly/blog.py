

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from teamly.state import ConnectionState
    from .types.blog import Blog as BlogPayload

__all__ = [
    "Blog"
]


class Blog:

    __slots__ = (
        '_state',
        'id',
        'title',
        'content',
        '_created_at',
        '_created_by',
        '_edited_at',
        '_team_id',
        '_hero_image'
    )

    def __init__(self, state: ConnectionState, data: BlogPayload) -> None:
        self._state: ConnectionState = state
        self._update(data)

    def _update(self, data: BlogPayload):
        self.id: str = data['id']
        self.title: str = data['title']
        self.content: str = data['content']

        self._created_at: str = data['createdAt']
        self._created_by: str = data['createdBy']
        self._edited_at: Optional[str] = data.get('editedAt')
        self._team_id: str = data['teamId']
        self._hero_image: Optional[str] = data.get('heroImage')

    @property
    def createdAt(self):
        return self._created_at

    @property
    def createdBy(self):
        return self._created_by

    @property
    def editedAt(self):
        return self._edited_at if self._edited_at else None

    @property
    def teamId(self):
        return self._team_id

    @property
    def heroImage(self):
        return self._hero_image if self._hero_image else None



    def to_dict(self):
        result = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "createdAt": self._created_at,
            "createdBy": self._created_by,
            "editedAt": self._edited_at,
            "teamId": self._team_id,
            "heroImage": self._hero_image
        }

        return result
