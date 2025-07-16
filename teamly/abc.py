
from __future__ import annotations

from .http import message_handler
from enum import Enum
from typing import Any, Dict, List, Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from .state import ConnectionState

class ChannelType(str, Enum):
    TEXT = 'text'
    VOICE = 'voice'
    TODO = 'todo'
    WATCHSTREAM = 'watchstream'
    ANNOUNCEMENT = 'announcement'

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Status(int,Enum):
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2
    DO_DO_DISTURB = 3

StatusLiteral = Literal[Status.OFFLINE, Status.ONLINE, Status.IDLE, Status.DO_DO_DISTURB]



class MessageAble:

    def __init__(self,state: ConnectionState) -> None:
        self._state: ConnectionState = state

    async def send(
        self,
        content: str,
        *,
        embeds: str = None,
        attachment: List[Dict[str,Any]] = None,
        replyTo: str = None
    ):
        payload = await message_handler(
            content,
            embeds=embeds,
            attachment=attachment,
            replyTo=replyTo
        )

        return await self._state.http.create_message(self.channel_id, payload)
