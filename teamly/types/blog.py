


from __future__ import annotations

from typing import Optional, TypedDict


class Blog(TypedDict):
    id: str
    title: str
    content: str
    createdAt: str
    createdBy: str
    editedAt: Optional[str]
    teamId: str
    heroImage: Optional[str]
