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

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from teamly.state import ConnectionState
    from .types.blog import Blog as BlogPayload
    from .team import Team

__all__ = [
    "Blog"
]


class Blog:

    __slots__ = (
        '_state',
        'id',
        'title',
        'content',
        'created_at',
        'created_by',
        'edited_at',
        'team',
        'hero_image'
    )

    def __init__(
        self,
        *,
        state: ConnectionState,
        team: Team,
        data: BlogPayload
    ) -> None:
        self._state: ConnectionState = state
        self.team: Team = team

        self.id: str = data['id']
        self.title: str = data['title']
        self.content: str = data['content']

        self.created_at: str = data['createdAt']
        self.created_by: str = data['createdBy']
        self.edited_at: Optional[str] = data.get('editedAt')
        self.hero_image: Optional[str] = data.get('heroImage')


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "createdAt": self.created_at,
            "createdBy": self.created_by,
            "editedAt": self.edited_at,
            "teamId": self.team.id,
            "heroImage": self.hero_image
        }

    def __repr__(self) -> str:
        return f"<Blog id={self.id} title={self.title!r} content={self.content!r}>"
