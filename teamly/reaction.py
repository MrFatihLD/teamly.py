
from __future__ import annotations

from teamly.user import User




from .types.reaction import Reaction as ReactionPayload
from typing import TYPE_CHECKING, Mapping, List

if TYPE_CHECKING:
    from .state import ConnectionState
    from .message import Message
    from .abc import MessageAbleChannel

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
        channel: MessageAbleChannel,
        message: Message,
        data: ReactionPayload
    ) -> None:
        self._state: ConnectionState = state
        self.channel: MessageAbleChannel = channel
        self.message: Message = message
        self._update(data)

    def _update(self, data: Mapping):
        self._emoji_id: str = data['emojiId']
        self.team_id: str = data['teamId']
        self.user: User = User(state=self._state, data=data['reactedBy'])

    @property
    def emojiId(self):
        return self._emoji_id

    def __repr__(self) -> str:
        return f"<Reaction emojiId={self._emoji_id} username={self.user.username}>"
