



from typing import Optional, TypedDict

class EmbedAuthor(TypedDict):
    name: str
    icon_url: str

class EmbedMedia(TypedDict):
    url: str

class EmbedFooter(TypedDict):
    text: str
    icon_url: str

class Embed(TypedDict):
    title: str
    description: str
    url: Optional[str]
    color: Optional[int]
    author: EmbedAuthor
    thumbnail: EmbedMedia
    image: EmbedMedia
    footer: EmbedFooter
