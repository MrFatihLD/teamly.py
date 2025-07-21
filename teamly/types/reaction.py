

from __future__ import annotations

from typing import TypedDict

from teamly.user import User


class Reaction(TypedDict):
    messageId: str
    channelType: str
    emojiId: str
    channelId: str
    teamId: str
    reactedBy: User
