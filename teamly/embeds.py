

from __future__ import annotations

from typing import Any, Dict, Optional

class Embed:

    def __init__(self, data: Dict[str, Any]) -> None:
        self.title: Optional[str] = data.get('title', None)
        self.description: Optional[str] = data.get('description', None)
        self.url: Optional[str] = data.get('url', None)
        self.color: Optional[str] = data.get('color', None)
        self.author: Optional[Dict[str, str]] = data.get('author', {})
        self.thumbnail: Optional[str] = data.get('thumbnail', {})
        self.image: Optional[str] = data.get('image', {})
        self.footer: Optional[Dict[str,str]] = data.get('footer', {})
