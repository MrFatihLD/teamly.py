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

from .types.embed import Embed as EmbedPayload
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from .state import ConnectionState

class Embed:

    def __init__(self, state: ConnectionState, data: EmbedPayload) -> None:
        self._state: ConnectionState = state
        self.title: Optional[str] = data.get('title')
        self.description: Optional[str] = data.get('description')
        self.url: Optional[str] = data.get('url')
        self.color: Optional[int] = data.get('color')
        self.author: Optional[Dict] = data.get('author')
        self.thumbnail: Optional[Dict] = data.get('thumbnail')
        self.image: Optional[Dict] = data.get('image')
        self.footer: Optional[Dict] = data.get('footer')

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "color": self.color,
            "author": self.author,
            "thumbnail": self.thumbnail,
            "image": self.image,
            "footer": self.footer
        }
