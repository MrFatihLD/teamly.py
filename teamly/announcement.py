
from __future__ import annotations

from asyncio.timeouts import Optional

from .types.announcement import Announcement as AnnouncementPayload
from .user import User
from .reaction import Reaction

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from .state import ConnectionState

class Announcement:

    def __init__(self, state: ConnectionState, data: AnnouncementPayload) -> None:
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.title: str = data['title']
        self.content: str = data['content']
        self.created_by: User = User(state=state,data=data['createdBy'])

        self.attachments: Optional[List[Dict[str,str]]] = data.get('attachments', [])
        self.emojis: Optional[List[Dict[str,str]]] = data.get('emojis', [])
        self.mentions: Optional[List[str]] = data.get('mentions', [])
        self.reactions: Optional[List[Reaction]] = [Reaction(r) for r in data.get('reactions', [])]

        self.created_at: str = data['createdAt']
        self.edited_at: Optional[str] = data.get('editedAt', None)


    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title} content={self.content}>"
