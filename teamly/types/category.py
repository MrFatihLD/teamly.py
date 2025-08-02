

from typing import Dict, Literal, Optional, TypedDict

class CategoryPermissions(TypedDict):
    roleId: str
    allow: str
    deny: str

class Category(TypedDict):
    id: str
    teamId: str
    name: str
    createdBy: str
    priority: Optional[int]
    permissions: Dict[Literal['role'],CategoryPermissions]
    createdAt: str
    editedAt: Optional[str]
