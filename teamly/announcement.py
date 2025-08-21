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

from teamly.user import User
from .types.announcement import (
    Announcement as AnnouncementPayload,
    AnnouncementEmojis,
    AnnouncementMedia,
    AnnouncementMentions,
    AnnouncementReactions as AnnouncementReactionsPayload)
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .state import ConnectionState
    from .channel import AnnouncementChannel


class Announcement:

    __slots__ = (
        "_state",
        "channel",
        "id",
        "title",
        "content",
        "created_by",
        "_attachments",
        "_emojis",
        "_mentions",
        "_reactions",
        "created_at",
        "edited_at"
    )

    def __init__(
        self,
        *,
        state: ConnectionState,
        channel: AnnouncementChannel,
        data: AnnouncementPayload
    ) -> None:
        self._state: ConnectionState = state
        self.channel = channel

        self.id: str = data['id']
        self.title: str = data['title']
        self.content: str = data['content']

        self.created_by: User = User(state=self._state, data=data['createdBy'])
        self._attachments: Optional[List[AnnouncementMedia]] = data.get('attachments')
        self._emojis: Optional[List[AnnouncementEmojis]] = data.get('emojis')
        self._mentions: Optional[AnnouncementMentions] = data.get('mentions')
        self._reactions: Optional[List[AnnouncementReactionsPayload]] = data.get('reactions')

        self.created_at: str = data['createdAt']
        self.edited_at: Optional[str] = data.get('editedAt')

    def to_dict(self):
        return {
            "id": self.id,
            "channelId": self.channel.id,
            "title": self.title,
            "content": self.content,
            "createdBy": self.created_by,
            "attachments": self._attachments,
            "emojis": self._emojis,
            "mentions": self._mentions,
            "reactions": self._reactions,
            "createdAt": self.created_at,
            "editedAt": self.edited_at
        }

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title!r} channelId={self.channel.id}>"
