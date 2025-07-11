

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

class _BaseChannel(TypedDict):
    id: str
    type: str
    teamId: str
    name: str
    description: Optional[str]

class _ChannelPayload(_BaseChannel):
    createdBy: str
    parentId: Optional[str]
    priority: int
    createdAt: str
    permissions: Dict[str,Any]
    additionalData: Optional[Dict[str,Any]]

class TextChannelPayload(_ChannelPayload):
    rateLimitPerUser: int

class VoiceChannelPayload(_ChannelPayload):
    participants: Optional[List[str]]
