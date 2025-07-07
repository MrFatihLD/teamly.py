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



from .state import ConnectionState
from .embed import Embed
from .emoji import Emoji
from .reaction import Reaction
from .mention import Mentions

from types.message import MessagePayload, MessageAttachment

from typing import Optional, List

class Attachment:

    def __init__(self, data: MessageAttachment) -> None:
        self.url: str = data.get('url', None)
        self.name: str = data.get('name')
        self.file_size_bytes: int = data.get('fileSizeBytes', None)

    def __repr__(self) -> str:
        return f"<Attachment name={self.name!r} size={self.size}B url={self.url}>"

    @property
    def file_extension(self) -> str:
        filename = self.name
        return filename.rsplit('.', 1)[-1].lower() if '.' in self.name else ''

    @property
    def is_image(self) -> bool:
        return self.file_extension in {"png","jpg","jpeg","gif","webp"}

    @property
    def is_video(self) -> bool:
        return self.file_extension in {"mp4","mov","webm"}

    @property
    def is_audio(self) -> bool:
        return self.file_extension in {"mp3","wav","ogg"}


class Message:

    def __init__(self, state: ConnectionState, data: MessagePayload) -> None:
        self._state: ConnectionState = state

        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.type: str = data['type']
        self.content: Optional[str] = data.get('content', None)
        self.attachment: List[Attachment] = [Attachment(a) for a in data.get('attachments', None)]
        #createdBy -> User
        self.edited_at: Optional[str] = data['editedAt']
        self.reply_to: Optional[str] = data.get('replyTo', None)
        self.embeds: List[Embed] = [Embed(a) for a in data.get('embeds', None)]
        self.emojis: List[Emoji] = [Emoji(a) for a in data.get('emojis', None)]
        self.reactions: List[Reaction] = [Reaction(r) for r in data.get('reactions', None)]
        self.nonce: Optional[str] = data.get('nonce', None)
        self.created_at: str = data['createdAt']
        self.mentions: Mentions = Mentions(data.get('mentions', {}))


    @property
    def author(self):
        pass

    @property
    def channel(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def copy(self):
        pass

    def reply(self):
        pass

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return ""
