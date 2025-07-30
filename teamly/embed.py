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

from typing import Optional, Dict, Self
from .types.embed import Embed as EmbedPayload
from .color import Color

class Embed:

    __slots__ = (
        'title',
        'description',
        'url',
        'color',
        '_author',
        '_thumbnail',
        '_image',
        '_footer'
    )

    def __init__(self, data: EmbedPayload) -> None:
        self.title: Optional[str] = data.get("title")
        self.description: Optional[str] = data.get("description")
        self.url: Optional[str] = data.get("url")
        self.color: Optional[Color] = Color(data["color"]) if data.get("color") is not None else None
        self._author: Optional[Dict[str,str]] = data.get("author")
        self._thumbnail: Optional[Dict[str,str]] = data.get("thumbnail")
        self._image: Optional[str] = data.get("image")
        self._footer: Optional[Dict[str,str]] = data.get("footer")

    def to_dict(self):
        payload = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "color": self.color,
            "author": self._author,
            "thumbnail": self._thumbnail,
            "image": self._image,
            "footer": self._footer
        }

        return payload

    @property
    def author(self):
        if self._author:
            return self._author.get("name"),self._author.get("icon_url")

    @property
    def thumbnail(self):
        if self._thumbnail:
            return self._thumbnail["url"]

    @property
    def image(self):
        if self._image:
            return self._image["url"]

    @property
    def footer(self):
        if self._footer:
            return self._footer.get("text"),self._footer.get("icon_url")

    @classmethod
    def new(
        cls,
        title: Optional[str] = None,
        *,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[Color] = None,
        author_name: Optional[str] = None,
        author_icon_url: Optional[str] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer_text: str = None,
        footer_icon_url: str = None
    ) -> Self:
        self = cls.__new__(cls)

        if len(title) > 16:
            raise ValueError("The title is to long, title should 16 or less then 16 characters")
        self.title = title

        if len(description) > 1024:
            raise ValueError("The description is to long, description should 1024 or less then 1012 characters")
        self.description = description

        self.url = url
        self.color = color

        if author_name:
            if len(author_name) > 16:
                raise ValueError("The author name is to long, author name should 16 or less then 16 characters")
        self._author = {"name":author_name,"icon_url": author_icon_url}

        self._thumbnail = {"url": thumbnail}
        self._image = {"url": image}

        if footer_text:
            if len(footer_text) > 16:
                raise ValueError("The footer text is to long, footer text should 16 or less then 16 characters")
        self._footer = {"text":footer_text,"icon_url":footer_icon_url}

        return self
