

from typing import TypedDict, Optional



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

class Embed(TypedDict):
    title: Optional[str] #Title of the embed; <= 16 characters
    description: Optional[str] #Description text for the embed (Markdown supported); <= 1024 characters
    url: Optional[str] #URL associated with the embed
    color: Optional[int] #Color code for the embed, represented in hexadecimal format
    author: Optional[EmbedAuthor] #Contains information about the author of the embed
    thumbnail: Optional[EmbedThumbnail] #Contains information about the thumbnail image
    image: Optional[EmbedImage] #Contains information about the image
    footer: Optional[EmbedFooter] #Contains information about the footer
