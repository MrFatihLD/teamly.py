


from __future__ import annotations


from typing import Any, Dict, List, Optional, TypedDict

from .embed import Embed
from teamly.user import User

class Message(TypedDict):
    id: str
    channelId: str
    type: str
    content: Optional[str]
    attachments: Optional[List[str]]
    createdBy: User
    editedAt: Optional[str]
    replyTo: Optional[str]
    embeds: Optional[List[Embed]]
    emojis: Optional[List[Dict[str,str]]]
    reactions: Optional[List[Dict[str,Any]]]
    nonce: Optional[str]
    createdAt: str
    mentions: Dict[str,List[str]]
