

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

class BaseChannel(TypedDict):
    id: str
    type: str
    teamId: str
    name: str
    description: Optional[str]
    createdBy: str
    parentId: Optional[str]
    priority: int
    createdAt: str
    permissions: Dict[str,Any]
    additionalData: Optional[Dict[str,Any]]

class TextChannelPayload(BaseChannel):
    rateLimitPerUser: int

class VoiceChannelPayload(BaseChannel):
    participants: Optional[List[str]]
