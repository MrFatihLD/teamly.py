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

from typing import Dict, Any, TYPE_CHECKING, Optional
from .user import User

if TYPE_CHECKING:
    from .state import ConnectionState

class Message:

    def __init__(self, state: ConnectionState ,data: Dict[str, Any]) -> None:
        self.state: ConnectionState = state
        self.data: Dict[str, Any] = data

        self.id = self.data['id']
        self.channelid = self.data['channelId']
        self.type = self.data['type']
        self.content: str = self.data['content']
        self.embeds = self.data['embeds']
        self.attachments = self.data['attachments']
        #editedAt
        #replyTo
        #emojis
        #reactions
        #nonce
        #isPinned
        #createdAt

    @classmethod
    def _copy(cls, state: ConnectionState, data: Dict[str, Any]):
        pass

    @property
    def author(self) -> User:
        createdby = User(createdby=self.data['createdBy'])
        return createdby

    async def send(self, content: str, replyTo: Optional[str] = None):
        messageid = self.data['channelId']
        payload = {"content":content,"replyTo":replyTo}
        await self.state.http.create_message(messageid,payload)
