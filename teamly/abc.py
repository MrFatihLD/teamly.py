
from __future__ import annotations



from .http import message_handler
from typing import Any, Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from .state import ConnectionState




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

        return await self._state.http.create_message(self.channel.id, payload)
