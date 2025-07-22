

from __future__ import annotations

from typing import List, Optional, TypedDict

from teamly.user import User

class AnnouncementMedia(TypedDict):
    url: str

class AnnouncementEmojis(TypedDict):
    emojiId: str

class AnnouncementMentions(TypedDict):
    users: List[str]

class AnnouncementReactedUsers(TypedDict):
    userId: str
    timestamp: str

class AnnouncementReactions(TypedDict):
    emojiId: Optional[str]
    count: Optional[int]
    users: Optional[List[AnnouncementReactedUsers]]


class Announcement(TypedDict):
    id: str
    channelId: str
    title: str
    content: str
    createdBy: User
    attachments: Optional[List[AnnouncementMedia]]
    emojis: Optional[List[AnnouncementEmojis]]
    mentions: AnnouncementMentions
    reactions: List[AnnouncementReactions]
    createdAt: str
    editedAt: Optional[str]
