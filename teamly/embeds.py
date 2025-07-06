

from __future__ import annotations

from typing import Any, Dict, Optional

class EmbedAuthor:
    def __init__(self, data: Dict[str,Any]) -> None:
        self.name: Optional[str] = data.get('name', None)
        self.icon_url: Optional[str] = data.get('icon_url', None)

class EmbedThumbnail:
    def __init__(self, data: Dict[str,Any]) -> None:
        self.url: Optional[str] = data.get('url', None)

class EmbedImage:
    def __init__(self, data: Dict[str,Any]) -> None:
        self.url: Optional[str] = data.get('url', None)

class EmbedFooter:
    def __init__(self, data: Dict[str,Any]) -> None:
        self.text: Optional[str] = data.get('text', None)
        self.icon_url: Optional[str] =data.get('icon_url', None)

class Embed:

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

        self.title: Optional[str] = data.get('title', None)
        self.description: Optional[str] = data.get('description', None)
        self.url: Optional[str] = data.get('url', None)
        self.color: Optional[str] = data.get('color', None)


    @property
    def author(self) -> EmbedAuthor:
        return EmbedAuthor(self.data['author']) #type: ignore

    @property
    def thumbnail(self) -> EmbedThumbnail:
        return EmbedThumbnail(self.data['thumbnail'])

    @property
    def image(self) -> EmbedImage:
        return EmbedImage(self.data['image'])

    @property
    def footer(self) -> EmbedFooter:
        return EmbedFooter(self.data['footer'])
