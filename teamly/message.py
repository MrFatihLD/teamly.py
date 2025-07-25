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

import teamly.abc

from .reaction import PartialReaction
from .user import User
from .embed import Embed
from .types.message import Message as MessagePayload
from typing import TYPE_CHECKING, Dict, List, Optional, Union

if TYPE_CHECKING:
    from teamly.state import ConnectionState

    from .channel import TextChannel
    from .team import Team

    MessageAbleChannel = Union[TextChannel]


class Message(teamly.abc.MessageAble):

    __slots__ = (
        '_state',
        'id',
        'channel',
        'type',
        '_content',
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
        team: Team,
        channel: MessageAbleChannel,
        data: MessagePayload
    ) -> None:
        super().__init__(state=state)
        self._state: ConnectionState = state
        self.channel: MessageAbleChannel = channel
        self.team: Team = team
        self.from_dict(data)

    def from_dict(self, data: MessagePayload):
        self.id: str = data['id']
        self.type: str = data['type']
        self._content: str = data['content']

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
        """
        Returns the user who created (authored) the message.

        This property provides access to the original author of the message.
        It returns a `User` instance representing the user who sent or created the message.

        Returns:
            User: The user who authored the message.
        """
        return self._created_by

    @property
    def content(self) -> str:
        """
        Gets the message's text content.

        Returns:
            str: The message body.
        """
        return self.content

    @property
    def attachment(self) -> List[str | None]:
        if self._attachment:
            return [x.get('url') for x in self._attachment]
        else:
            return []

    @property
    def repliedTo(self) -> str | None:
        """
        Gets the ID of the user this message is replying to.

        Returns:
            Optional[int]: The user ID, or None if the message is not a reply.
        """
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
    def emojis(self) -> List[str | None]:
        """
        Returns a list of emoji IDs used in the message.

        This method extracts and returns the IDs of all emojis present in the message content.
        If the message does not contain any emojis, it returns an empty list.

        Returns:
            List[int]: A list of emoji IDs found in the message. Empty if none are present.
        """
        if self._emojis:
            return [e.get('emojiId') for e in self._emojis]
        else:
            return []

    @property
    def reactions(self) -> List[PartialReaction | None]:
        if self._reactions:
            return [PartialReaction(r) for r in self._reactions]
        else:
            return []

    @property
    def mentions(self) -> List[str] | None:
        """
        Returns a list of user IDs mentioned in the message.

        This method extracts all user mentions from the message content and
        returns their corresponding user IDs. If no users are mentioned, it returns an empty list.

        Returns:
            List[int]: A list of mentioned user IDs. Empty if no mentions are present.
        """
        if self._mentions:
            return self._mentions['users']

    def to_dict(self):
        result = {
            "id": self.id,
            "channelId": self.channel.id,
            "type": self.type,
            "content": self._content,
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

    class PrivateMessage:
        pass
