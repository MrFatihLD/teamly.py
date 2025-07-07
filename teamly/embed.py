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

from .types.embed import EmbedFooterProxy, EmbedImageProxy, EmbedPayload, EmbedAuthorProxy, EmbedThumbnailProxy

from typing import Optional, Union

class EmbedAuthor:
    def __init__(self, data: EmbedAuthorProxy) -> None:
        self.name: Optional[str] = data['name']
        self.icon_url: Optional[str] = data['icon_url']

    def __repr__(self) -> str:
        return f"<EmbedAuthor name={self.name!r}"

class EmbedMedia:
    def __init__(self, data: Union[EmbedThumbnailProxy,EmbedImageProxy]) -> None:
        self.url: Optional[str] = data.get("url", None)

    def __repr__(self) -> str:
        return f"<EmbedMedia url={self.url!r}>"

class EmbedFooter:
    def __init__(self, data: EmbedFooterProxy) -> None:
        self.text: Optional[str] = data.get("text", None)
        self.icon_url: Optional[str] = data.get("icon_url", None)

    def __repr__(self) -> str:
        return f"<EmbedFooter text={self.text!r}>"

class Embed:

    def __init__(self, data: EmbedPayload) -> None:
        self.title: Optional[str] = data.get('title', None)
        self.description: Optional[str] = data.get('description', None)
        self.url: Optional[str] = data.get('url', None)
        self.color: Optional[int] = data.get('color', None)

        self.author: Optional[EmbedAuthor] = (
            EmbedAuthor(data.get('author', None))
        )

        self.thumbnail: Optional[EmbedMedia] = (
            EmbedMedia(data.get('thumbnail', None))
        )

        self.image: Optional[EmbedMedia] = (
            EmbedMedia(data.get('image', None))
        )

        self.footer: Optional[EmbedFooter] = (
            EmbedFooter(data.get('footer', None))
        )

    def __repr__(self) -> str:
        return f"<Embed title={self.title!r} description={self.description!r}>"
