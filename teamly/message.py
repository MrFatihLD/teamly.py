

from __future__ import annotations

from .reaction import PartialReaction
from teamly.abc import MessageAble, MessageAbleChannel
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
        'channel',
        'type',
        'content',
        '_attachment',
        '_created_by',
        'edited_at',
        '_reply_to',
        '_embeds',
        '_emojis',
        '_reactions',
        'nonce',
        'created_at',
        '_mentions'
    )

    def __init__(
        self,
        state: ConnectionState,
        *,
        channel: MessageAbleChannel,
        data: MessagePayload
    ) -> None:
        super().__init__(state=state)
        self._state: ConnectionState = state
        self.channel: MessageAbleChannel = channel
        self.from_dict(data)

    def from_dict(self, data: MessagePayload):
        self.id: str = data['id']
        self.type: str = data['type']
        self.content: Optional[str] = data.get('content')

        self._attachment: Optional[List[Dict[str,str]]] = data.get('attachments')
        self._created_by: User = User(state=self._state, data=data['createdBy'])
        self.edited_at: Optional[str] = data.get('editedAt')
        self._reply_to: Optional[str] = data.get('replyTo')
        self._embeds: Optional[List[Embed]] = data.get('embeds')
        self._emojis: Optional[List[Dict[str,str]]] = data.get('emojis')
        self._reactions: Optional[List[Dict[str,str]]] = data.get('reactions')
        self.nonce: Optional[str] = data.get('nonce')
        self.created_at: str = data['createdAt']
        self._mentions: Dict[str,List[str]] = data.get('mentions')

    @property
    def author(self) -> User:
        return self._created_by

    @property
    def attachment(self):
        if self._attachment:
            return [x.get('url') for x in self._attachment]
        else:
            return []

    @property
    def repliedTo(self):
        if self._reply_to:
            return self._reply_to
        else:
            return None

    @property
    def embeds(self):
        if self._embeds:
            return [Embed.from_dict(e) for e in self._embeds]
        else:
            return []

    @property
    def emojis(self):
        if self._emojis:
            return [e.get('emojiId') for e in self._emojis]
        else:
            return []

    @property
    def reactions(self):
        if self._reactions:
            return [PartialReaction(r) for r in self._reactions]
        else:
            return []

    @property
    def mentions(self):
        if self._mentions:
            return self._mentions['users']

    def to_dict(self):
        result = {
            "id": self.id,
            "channelId": self.channel.id,
            "type": self.type,
            "content": self.content,
            "createdBy": self.author.to_dict(),
            "createdAt": self.created_at
        }
        if self.attachment:
            result['attachment'] = self._attachment
        if self.edited_at:
            result['editedAt'] = self.edited_at
        if self._reply_to:
            result['replyTo'] = self._reply_to
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

        return result

    def __repr__(self) -> str:
        return (
            f"<Message id={self.id} channelId={self.channel.id} type={self.type} content={self.content} "
            f"createdBy={self.author.username}>"
        )
