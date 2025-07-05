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

from typing import TYPE_CHECKING, List, Optional, Any
from .user import User
from .types.message import MessagePayload

if TYPE_CHECKING:
    from .state import ConnectionState


class Message:

    def __init__(self, state: ConnectionState ,data: MessagePayload) -> None:
        self._state: ConnectionState = state

        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: str = data.get('content', None)
        self.attachments: Optional[List[str]] = data.get('attachments', [])
        self.embeds: List[Any] = data.get('embeds', []) #temporaly
        self.created_by: User = User(data=data['createdBy'])
        self.editedAt: Optional[str] = data.get('editedAt', None)
        self.reply_to: Optional[str] = data.get('replyTo', None)
        self.emojis: List[Any] = data.get('emojis', []) #temporaly
        self.reactions: List[Any] = data.get('reactions', []) #temporaly
        self.nonce: Optional[str] = data['nonce']
        self.is_pinned: bool = data['isPinned']
        self.created_at: str = data['createdAt']

    @property
    def author(self) -> User:
        return self.createdBy

    async def send(self, content: str, replyTo: Optional[str] = None):
        channel_id = self.channel_id
        payload = {"content":content,"replyTo":replyTo}
        await self._state.http.create_message(channel_id,payload)

    async def reply(self, content: str):
        payload = {"content": content,"replyTo": self.id}
        await self._state.http.create_message(self.channel_id,payload)
