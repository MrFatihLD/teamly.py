

from __future__ import annotations

from teamly.reaction import PartialReaction
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

class Announcement:

    def __init__(self, state: ConnectionState, data: AnnouncementPayload) -> None:
        self._state: ConnectionState = state
        self._update(data=data)

    def _update(self, data: AnnouncementPayload):
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.title: str = data['title']
        self.content: str = data['content']

        self._created_by: User = User(state=self._state, data=data['createdBy'])
        self._attachments: Optional[List[AnnouncementMedia]] = data.get('attachments')
        self._emojis: Optional[List[AnnouncementEmojis]] = data.get('emojis')
        self._mentions: Optional[AnnouncementMentions] = data.get('mentions')
        self._reactions: Optional[List[AnnouncementReactionsPayload]] = data.get('reactions')

        self._created_at: str = data['createdAt']
        self._edited_at: Optional[str] = data.get('editedAt')

    @property
    def user(self):
        return self._created_by

    @property
    def attachments(self):
        if self._attachments:
            return [x.get('url') for x in self._attachments]
        else:
            return []

    @property
    def emojis(self):
        if self._emojis:
            return [x.get('emojis') for x in self._emojis]
        else:
            return []

    @property
    def mentions(self):
        if self._mentions:
            return self._mentions['users']
        else:
            return []

    @property
    def reactions(self):
        if self._reactions:
            return [PartialReaction(r) for r in self._reactions]
        else:
            return []

    @property
    def createdAt(self):
        return self._created_at

    @property
    def editedAt(self):
        return self._edited_at

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title!r} channelId={self.channel_id}>"
