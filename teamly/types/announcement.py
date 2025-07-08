



from typing import Dict, List, TypedDict, Optional

from .mention import MentionPayload
from .reaction import ReactionPayload
from .user import UserPayload

class AnnouncementAttachment(TypedDict):
    url: Optional[str]

class Announcement(TypedDict):
    id: str
    channelId: str
    title: str
    content: str
    createdBy: UserPayload
    attachments: List[AnnouncementAttachment]
    emojis: List[Dict[str,str]]
    mentions: MentionPayload
    reactions: List[ReactionPayload]
    createdAt: str
    editedAt: Optional[str]
