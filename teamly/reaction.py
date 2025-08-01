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




from .types.reaction import Reaction as ReactionPayload, CustomReaction as CustomReactionPayload
from typing import TYPE_CHECKING, Mapping, List, Union, Any

if TYPE_CHECKING:
    from .state import ConnectionState
    from .team import Team
    from .message import Message
    from .channel import TextChannel

    MessageAbleChannel = Union[TextChannel]

class PartialReaction:

    def __init__(self, data: dict) -> None:
        self._emoji_id: str = data.get('emojiId')
        self._count: int = data.get('count')
        self._users: List[dict] = data.get('users')

    @property
    def emojiId(self):
        return self._emoji_id

    @property
    def count(self):
        return self._count

    @property
    def users(self):
        return [[u.get('userId'),u.get('timestamp')] for u in self._users]

class Reaction:

    def __init__(
        self,
        *,
        state: ConnectionState,
        team: Team,
        channel: MessageAbleChannel,
        message: Message,
        data: ReactionPayload
    ) -> None:
        self._state: ConnectionState = state
        self.team: Team = team
        self.channel: MessageAbleChannel = channel
        self.message: Message = message
        self._update(data)

    def _update(self, data: Mapping):
        self._emoji_id: str = data['emojiId']
        self.user: User = User(state=self._state, data=data['reactedBy'])

    @property
    def emojiId(self):
        return self._emoji_id

    def __repr__(self) -> str:
        return f"<Reaction emojiId={self._emoji_id} username={self.user.username}>"

class CustomReaction:

    __slots__ = (
        '_state',
        'id',
        'name',
        'created_by',
        'updated_by',
        'updated_at',
        'url',
        'created_at'
    )

    def __init__(self, state: ConnectionState, data: CustomReactionPayload) -> None:
        self._state: ConnectionState = state

        self.id: str = data['id']
        self.name: str = data['name']
        self.created_by: str = data['createdBy']
        self.updated_by: str = data.get('updatedBy')
        self.updated_at: str = data.get('updatedAt')
        self.url: str = data['url']
        self.created_at: str = data['createdAt']

    @classmethod
    def new(cls, name: str, emoji: Any):
        self = cls.__new__(cls)

        self.name = name
        self.emoji = emoji

        return {"name":name,"emoji":emoji}

    def __repr__(self) -> str:
        return f"<CustomReaction id={self.id} name={self.name} url={self.url}>"
