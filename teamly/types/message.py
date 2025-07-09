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

from .user import UserPayload
from .emoji import Emoji as EmojiPayload
from .embed import EmbedPayload
from typing import List, TypedDict, Optional




class MessageAttachment(TypedDict):
    url: str
    name: str
    fileSizeBytes: int

class _MessageReactedUsers(TypedDict):
    userId: Optional[str] #User ID who reacted
    timestamp: Optional[str] #Timestamp of the user's reaction

class MessageReactions(TypedDict):
    emojiId: Optional[str] #The emoji used for the reaction
    count: Optional[str] #Number of users who reacted with this emoji
    users: Optional[List[_MessageReactedUsers]]

class MessagePayload(TypedDict):
    id: str #Unique identifier for the message
    channelId: str #ID of the channel where the message was posted
    type: str #Type of the message (e.g., 'text' for a text message)
    content: str #Content of the message (Markdown supported); <= 2000 characters
    attachments: List[MessageAttachment] # Attachments for the message (may be empty); <= 5 items
    createdBy: UserPayload #User who created the message
    editedAt: str #Timestamp of when the message was last edited
    replyTo: str #ID of the message being replied to, or null if the message is not a reply
    embeds: List[EmbedPayload] #List of embeds included with the message; <= 5 items
    emojis: List[EmojiPayload] #The emoji used in the message
    reactions: List[MessageReactions]
    nonce: Optional[str] #Unique identifier for this message instance, used to prevent duplicates
    isPinned: bool
    createdAt: str #Timestamp of when the message was created
    mentions: List[Optional[str]] #Information about users mentioned in the message
