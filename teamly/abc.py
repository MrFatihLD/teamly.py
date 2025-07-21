
from __future__ import annotations


from teamly.channel import TextChannel, VoiceChannel

from .http import message_handler
from .enums import Status
from typing import Any, Dict, List, Literal, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from .state import ConnectionState




StatusLiteral = Literal[Status.OFFLINE, Status.ONLINE, Status.IDLE, Status.DO_DO_DISTURB]

MessageAbleChannel = Union[TextChannel, VoiceChannel]

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
