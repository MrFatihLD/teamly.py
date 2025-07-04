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


from .user import User
from .emoji import Emoji
from typing import List, TypedDict, Optional


class EmbedAuthor(TypedDict):
    name: Optional[str] #Name of the author; <= 12 characters
    icon_url: Optional[str] #URL to the author's icon

class EmbedThumbnail(TypedDict):
    url: Optional[str] #URL of the thumbnail image

class EmbedImage(TypedDict):
    url: Optional[str] #URL of the image to be displayed

class EmbedFooter(TypedDict):
    text: Optional[str] #Text content for the footer; <= 16 characters
    icon_url: Optional[str] #URL to the icon for the footer

class MessageEmbed(TypedDict):
    title: Optional[str] #Title of the embed; <= 16 characters
    description: Optional[str] #Description text for the embed (Markdown supported); <= 1024 characters
    url: Optional[str] #URL associated with the embed
    color: Optional[int] #Color code for the embed, represented in hexadecimal format
    author: Optional[EmbedAuthor] #Contains information about the author of the embed
    thumbnail: Optional[EmbedThumbnail] #Contains information about the thumbnail image
    image: Optional[EmbedImage] #Contains information about the image
    footer: Optional[EmbedFooter] #Contains information about the footer




class MessageAttachment(TypedDict):
    url: Optional[str]

class _MessageReactedUsers(TypedDict):
    userId: Optional[str] #User ID who reacted
    timestamp: Optional[str] #Timestamp of the user's reaction

class MessageReactions(TypedDict):
    emojiId: Optional[str] #The emoji used for the reaction
    count: Optional[str] #Number of users who reacted with this emoji
    users: Optional[List[_MessageReactedUsers]]

class Message(TypedDict):
    id: str #Unique identifier for the message
    channelId: str #ID of the channel where the message was posted
    type: str #Type of the message (e.g., 'text' for a text message)
    content: str #Content of the message (Markdown supported); <= 2000 characters
    attachments: Optional[List[MessageAttachment]] # Attachments for the message (may be empty); <= 5 items
    createdBy: User #User who created the message
    editedAt: str #Timestamp of when the message was last edited
    replyTo: str #ID of the message being replied to, or null if the message is not a reply
    embeds: List[MessageEmbed] #List of embeds included with the message; <= 5 items
    emojis: Optional[List[Emoji]] #The emoji used in the message
    reactions: List[MessageReactions]
    nonce: Optional[str] #Unique identifier for this message instance, used to prevent duplicates
    createdAt: str #Timestamp of when the message was created
    mentions: List[Optional[str]] #Information about users mentioned in the message
