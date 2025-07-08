




from typing import Optional, TypedDict
from .role import Permissions


class Category(TypedDict):
    id: str
    teamId: str
    name: str
    createdBy: str
    priority: Optional[Permissions]
    createdAt: str
    editedAt: str
