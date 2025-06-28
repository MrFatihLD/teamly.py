from ast import Not
from typing import List, NotRequired, TypedDict, Optional
from .user import User

class Attachments(TypedDict):
    url: str

class EmbedAuthor(TypedDict):
    name: NotRequired[str]
    icon_url: NotRequired[str]

class EmbedThumbnail(TypedDict):
    url: NotRequired[str]

class EmbedImage(TypedDict):
    url: NotRequired[str]

class EmbedFooter(TypedDict):
    text: NotRequired[str]
    icon_url: NotRequired[str]

class MessageEmbeds(TypedDict):
    title: Optional[str]
    description: Optional[str]
    url: NotRequired[Optional[str]]
    color: Optional[int]
    author: Optional[EmbedAuthor]
    thumbnail: Optional[EmbedThumbnail]
    image: Optional[EmbedImage]
    footer: Optional[EmbedFooter]

class MessageEmojis(TypedDict):
    emojiId: NotRequired[str]

class MessageReactionsUsers(TypedDict):
    userId: NotRequired[str]
    timestamp: NotRequired[str]

class MessageReactions(TypedDict):
    emojiId: NotRequired[str]
    count: NotRequired[int]
    users: NotRequired[List[MessageReactionsUsers]]

class MessageMentions(TypedDict):
    user: NotRequired[List[str]]

class Message(TypedDict):
    id: str
    channelId: str
    type: str
    content: Optional[str]
    attachments: NotRequired[Attachments]
    createdBy: User
    editedAt: Optional[str]
    replyTo: Optional[str]
    embeds: MessageEmbeds
    emojis: NotRequired[List[MessageEmojis]]
    reactions: NotRequired[List[MessageReactions]]
    nonce: NotRequired[str]
    createdAt: str
    mentions: MessageMentions
