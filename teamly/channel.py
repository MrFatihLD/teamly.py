

from __future__ import annotations



import datetime
from typing import Optional, Dict, List, Any


from types.channel import ChannelPayload

class Channel:

    def __init__(self, data: ChannelPayload) -> None:
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']
        self.description: Optional[str] = data.get("description", None)
        self.created_by: str = data['createdBy']
        self.created_at: Optional[datetime.datetime] = data['createdAt']
        self.parent_id: Optional[str] = data.get('parentId', None)

        if self.type == "voice":
            self.participants = [data['participants']]

        self.priority: int = data['priority']
        self.rate_limit_per_user: int = data['rateLimitPerUser']
        self.permissions: Dict[str,List[str]] = data.get('permissions', {})
        self.additional_data: Optional[Dict[str,Any]] = data.get('additionalData', {})
