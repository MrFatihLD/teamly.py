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

from .http import message_handler

from typing import List, TYPE_CHECKING, Optional, Union, Literal, overload


if TYPE_CHECKING:
    from .channel import TextChannel
    from .enums import Status
    from .state import ConnectionState
    from .embed import Embed
    from .attachment import Attachment

    MessageAbleChannel = Union[TextChannel]
    StatusLiteral = Literal[Status.OFFLINE, Status.ONLINE, Status.IDLE, Status.DO_DO_DISTURB]

class TeamChannel:
    pass

class MessageAble:

    def __init__(self,state: ConnectionState) -> None:
        self._state: ConnectionState = state

    @overload
    async def send(
        self,
        content: str,
        /
    ) -> None: ...

    @overload
    async def send(
        self,
        content: str,
        *,
        embeds: Embed
    ) -> None: ...

    @overload
    async def send(
        self,
        content: str,
        *,
        embeds: Embed,
        replyTo: Optional[str] = None
    ) -> None: ...

    @overload
    async def send(
        self,
        content: str,
        *,
        embeds: Optional[List[Embed]] = None,
        replyTo: Optional[str] = None
    ) -> None: ...

    async def send(
        self,
        content: Optional[str] = None,
        *,
        embeds: Union[Embed, Optional[List[Embed]], None] = None,
        attachments: Optional[List[Attachment]] = None,
        replyTo: Optional[str] = None
    ) -> None:

        if embeds is not None and embeds is not list:
            embeds = [embeds]

        payload = await message_handler(
            state=self._state,
            content=content,
            embeds=embeds,
            attachment=attachments,
            replyTo=replyTo
        )

        return await self._state.http.create_message(self.channel.id, payload)
