

from typing import Optional, Dict

from .color import Color


class Embed:
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[Color] = None
    ):
        if title and len(title) > 16:
            raise ValueError("title must be 16 characters or fewer")
        if description and len(description) > 1024:
            raise ValueError("description must be 1024 characters or fewer")

        self.title = title
        self.description = description
        self.url = url
        self.color = int(color) if color else None

        self.author: Optional[Dict[str, str]] = None
        self.thumbnail: Optional[Dict[str, str]] = None
        self.image: Optional[Dict[str, str]] = None
        self.footer: Optional[Dict[str, str]] = None

    def set_author(self, *, name: Optional[str] = None, icon_url: Optional[str] = None):
        self.author = {}
        if name:
            self.author["name"] = name
        if icon_url:
            self.author["icon_url"] = icon_url
        return self

    def set_thumbnail(self, *, url: str):
        self.thumbnail = {"url": url}
        return self

    def set_image(self, *, url: str):
        self.image = {"url": url}
        return self

    def set_footer(self, *, text: Optional[str] = None, icon_url: Optional[str] = None):
        self.footer = {}
        if text:
            self.footer["text"] = text
        if icon_url:
            self.footer["icon_url"] = icon_url
        return self

    def to_dict(self) -> Dict:
        data = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "color": self.color,
            "author": self.author,
            "thumbnail": self.thumbnail,
            "image": self.image,
            "footer": self.footer,
        }
        # Remove None values (Teamly muhtemelen boş objeleri istemez)
        return {k: v for k, v in data.items() if v is not None}
