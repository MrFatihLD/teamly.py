

from __future__ import annotations

from teamly.abc import MessageAble
from .user import User
from .embed import Embed
from .types.message import Message as MessagePayload
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from teamly.state import ConnectionState


class Message(MessageAble):

    __slots__ = (
        '_state',
        'id',
        'channel_id',
        'type',
        'content',
        'attachment',
        'created_by',
        'edited_at',
        'reply_to',
        'embeds',
        'emojis',
        'reactions',
        'nonce',
        'created_at',
        'mentions'
    )

    def __init__(self, state: ConnectionState, data: MessagePayload) -> None:
        super().__init__(state=state)
        self._state: ConnectionState = state
        self.from_dict(data)

    def from_dict(self, data: MessagePayload):
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: Optional[str] = data.get('content')

        self.attachment: Optional[List[Dict[str,str]]] = data.get('attachments')
        self.created_by: User = User(state=self._state, data=data['createdBy'])
        self.edited_at: Optional[str] = data.get('editedAt')
        self.reply_to: Optional[str] = data.get('replyTo')
        self.embeds: Optional[List[Embed]] = data.get('embeds')
        self.emojis: Optional[List[Dict[str,str]]] = data.get('emojis')
        self.reactions: Optional[List[Dict[str,str]]] = data.get('reactions')
        self.nonce: Optional[str] = data.get('nonce')
        self.created_at: str = data['createdAt']
        self.mentions: Dict[str,List[str]] = data.get('mentions')

    @property
    def author(self) -> User:
        return self.created_by

    def to_dict(self):
        result = {
            "id": self.id,
            "channelId": self.channel_id,
            "type": self.type,
            "content": self.content,
            "createdBy": self.created_by,
            "createdAt": self.created_at
        }
        if self.attachment:
            result['attachment'] = self.attachment
        if self.edited_at:
            result['editedAt'] = self.edited_at
        if self.reply_to:
            result['replyTo'] = self.reply_to
        if self.embeds:
            result['embeds'] = self.embeds
        if self.emojis:
            result['emojis'] = self.emojis
        if self.reactions:
            result['reactions'] = self.reactions
        if self.nonce:
            result['nonce'] = self.nonce
        if self.mentions:
            result['mentions'] = self.mentions

    def __repr__(self) -> str:
        return (
            f"<Message id={self.id} channelId={self.channel_id} type={self.type} content={self.content} "
            f"createdBy={self.created_by.username}>"
        )
