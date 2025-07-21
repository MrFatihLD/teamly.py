
from __future__ import annotations

from teamly.user import User



from .abc import MessageAbleChannel

from .types.reaction import Reaction as ReactionPayload
from typing import TYPE_CHECKING, Mapping

if TYPE_CHECKING:
    from .state import ConnectionState

class Reaction:

    def __init__(
        self,
        *,
        state: ConnectionState,
        channel: MessageAbleChannel,
        data: ReactionPayload
    ) -> None:
        self._state: ConnectionState = state
        self.channel: MessageAbleChannel = channel
        self._update(data)

    def _update(self, data: Mapping):
        self.message_id: str = data['messageId']
        self.emoji_id: str = data['emojiId']
        self.team_id: str = data['teamId']
        self.user: User = User(state=self._state, data=data['reactedBy'])

    def __repr__(self) -> str:
        return f"<Reaction emojiId={self.emoji_id} username={self.user.id}>"
