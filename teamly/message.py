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

from .embed import Embed

from .types.message import Message as MessagePayload
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from .state import ConnectionState

class Message:

    def __init__(self, state: ConnectionState, data: MessagePayload) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: str = data['content']
        self.attachments: Optional[List[Dict]] = data.get('attachments')
        self.created_by: str = data['createdBy']
        self.edited_at: str = data['editedAt']
        self.reply_to: Optional[str] = data.get('replyTo')
        self.embeds: Optional[List[Embed]] = [Embed(state=self._state, data=e) for e in data['embeds']] if data['embeds'] else []
        self.emojis: Optional[List[Dict]] = data.get('emojis', [])
        self.reactions: Optional[List[Dict]] = data.get('reactions', [])
        self.nonce: Optional[str] = data.get('nonce')
        self.created_at: str = data['createdAt']
        self.mentions: Optional[Dict[str, List[Dict]]] = data.get('mentions', {})

    def to_dict(self):
        return {
            "id": self.id,
            "channelId": self.channel_id,
            "type": self.type,
            "content": self.content,
            "attachments": self.attachments,
            "createdBy": self.created_by,
            "editedAt": self.edited_at,
            "replyTo": self.reply_to,
            "embeds": [e.to_dict() for e in self.embeds] if self.embeds else [],
            "emojis": self.emojis,
            "reactions": self.reactions,
            "nonce": self.nonce,
            "createdAt": self.created_at,
            "mentions": self.mentions
        }

    async def edit(self, content: str, embeds: Embed):
        payload = {"content": content, "embeds": [embeds]}
        await self._state.http.update_channel_message(channelId=self.channel_id, messageId=self.id, payload=payload)

    async def delete(self):
        await self._state.http.delete_message(channelId=self.channel_id, messageId=self.id)

    async def react(self, emojiId: str):
        await self._state.http.react_to_message(channelId=self.channel_id, messageId=self.id, emojiId=emojiId)

    async def delete_reaction(self, emojiId: str):
        await self._state.http.delete_reaction_from_message(channelId=self.channel_id, messageId=self.id, emojiId=emojiId)

    def __repr__(self) -> str:
        return f"<Message id={self.id} type={self.type} content={self.content} channelId={self.channel_id}>"
