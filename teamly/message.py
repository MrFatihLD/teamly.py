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
from teamly.member import Member

from .reaction import PartialReaction
from .user import User
from .embed import Embed
from .types.message import Message as MessagePayload
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from teamly.state import ConnectionState

    from .channel import TextChannel

    MessageAbleChannel = Union[TextChannel]


class Message(teamly.abc.MessageAble):
    '''Represents a user message.

    Attributese
    ------------
        id: :class:`str`
            Unique identifier for the message.
        channel: :class:`TextChannel`
            channel where the message was posted
        type: :class:`str`
            Type of the message (e.g., 'text' for a text message)
        content: :class:`str`
            Content of the message (Markdown supported)
        attachment: :class:`List[str | None]`
            Attachments for the message (may be empty)
        author: Union[:class:`Member`, :class:`User`]
            The user who sent the message. If the user is still in the server, this will be a
            :class:`Member` instance. If the user has left the server, it will be a :class:`User` instance instead.
        editedAt: :class:`str`
            Timestamp of when the message was last edited
        replie_to: :class:`str`
            ID of the message being replied to, or null if the message is not a reply
        embeds: :class:`List[str | None]`
            List of embeds included with the message
        emojis: :class:`List[str | None]`
            The emoji used in the message
        nonce: :class:`str`
            Unique identifier for this message instance, used to prevent duplicates
        createdAt: :class:`str`
            Timestamp of when the message was created
        mentions: :class:`List[str] | None`
            Information about users mentioned in the message
    '''

    author: Union[Member,User]

    __slots__ = (
        '_state',
        'id',
        'channel',
        'type',
        'content',
        '_attachment',
        'author',
        'edited_at',
        'reply_to',
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
        data: Dict
    ) -> None:
        super().__init__(state=state)
        self._state: ConnectionState = state
        self.channel: MessageAbleChannel = channel

        try:
            self.team = self.channel.team
        except AttributeError:
            self.team = self._state.cache.get_team(teamId=data['teamId'])

        self._update(data)

    def _update(self, data: MessagePayload):
        self.id: str = data['id']
        self.type: str = data['type']
        self.content: str = data['content']

        self._attachment: Optional[List[Dict[str,str]]] = data.get('attachments')

        try:
            self.author = self._state.cache.get_member(teamId=self.team.id,userId=data['createdBy']['id'])
        except AttributeError:
            self.author = User(state=self._state, data=data['createdBy'])

        self.edited_at: Optional[str] = data.get('editedAt')
        self.reply_to: Optional[Dict[str,Any]] = data.get('replyTo')
        self._embeds: Optional[List[Embed]] = data.get('embeds')
        self._emojis: Optional[List[Dict[str,str]]] = data.get('emojis')
        self._reactions: Optional[List[Dict[str,str]]] = data.get('reactions')
        self.nonce: Optional[str] = data.get('nonce')
        self.created_at: str = data['createdAt']
        self._mentions: Dict[str,List[str]] = data.get('mentions')


    @property
    def attachment(self) -> List[str | None]:
        if self._attachment:
            return [x.get('url') for x in self._attachment]
        else:
            return []

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
            "content": self.content,
            "createdBy": self.author.to_dict(),
            "createdAt": self.created_at
        }
        if self.attachment:
            result['attachment'] = self._attachment
        if self.edited_at:
            result['editedAt'] = self.edited_at
        if self.reply_to:
            result['replyTo'] = self.reply_to
        if self._embeds:
            result['embeds'] = self._embeds
        if self._emojis:
            result['emojis'] = self._emojis
        if self._reactions:
            result['reactions'] = self._reactions
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
