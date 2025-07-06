


from typing import TypedDict, Optional, List, Dict
from datetime import datetime


class RolePermissionEntry(TypedDict):
    roleId: Optional[str]
    allow: Optional[float]
    deny: Optional[float]

class Permissions(TypedDict):
    role: Dict[str, RolePermissionEntry]

class AdditionalData(TypedDict):
    streamChannel: Optional[str]
    streamPlatform: Optional[str]

class ChannelPayload(TypedDict):
    id: str
    type: str
    teamId: str
    name: str
    description: Optional[str]
    createdBy: str
    parentId: Optional[str]
    participants: Optional[List[str]]
    priority: float
    rateLimitPerUser: int  # 0 <= rateLimitPerUser <= 21600
    createdAt: datetime
    permissions: Permissions
    additionalData: Optional[AdditionalData]
