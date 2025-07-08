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


from .user import User
from .state import ConnectionState

from .types.channel import ChannelPayload, AdditionalData as AdditionalDataPayload, RolePermissionEntry
from typing import Optional, List, Any

class RolePermission:
    def __init__(self, role_id: str, data: RolePermissionEntry) -> None:
        self.role_id: str = role_id
        self.allow: int = data.get('allow', 0)
        self.deny: int = data.get('deny', 0)

    def __repr__(self) -> str:
        return f"<RolePermission role={self.role_id} allow={self.allow} deny={self.deny}>"

class ChannelPermissions:

    def __init__(self, data: Any) -> None:
        self.role_permissions: List[RolePermission] = []

        role_data = data.get('role', {})
        for role_id, perms in role_data.items():
            self.role_permissions.append(RolePermission(role_id,perms))

    def get(self, role_id: str) -> RolePermission | None:
        for rp in self.role_permissions:
            if rp.role_id == role_id:
                return rp
        return None

class AdditionalData:

    def __init__(self, data: AdditionalDataPayload) -> None:
        self.stream_channel: Optional[str] = data.get('streamChannel', None)
        self.stream_platform: Optional[str] = data.get('streamPlatform', None)

    def __repr__(self) -> str:
        return f"<AdditionalData steamChannel={self.stream_channel!r} streamPlatform={self.stream_platform}>"

class BaseChannel:

    def __init__(self,*,state: ConnectionState, data: ChannelPayload) -> None:
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']

        self.description: Optional[str] = data.get('description', None)
        self.created_by: User = User(state=state,data=data['createdBy'])
        self.parent_id: Optional[str] = data.get('parentId', None)
        self.priority: int = data['priority']
        self.rate_limit_per_user: int = data['rateLimitPerUser']
        self.created_at: str = data['createdAt']
        self.permissions: ChannelPermissions = ChannelPermissions(data['permissions']) if data['permissions'] is not None else {}
        self.additional_data: Optional[AdditionalData] = AdditionalData(data['additionalData']) if data['additionalData'] is not None else None



class VoiceChannel(BaseChannel):

    def __init__(self, *, state: ConnectionState, data: ChannelPayload) -> None:
        super().__init__(state=state, data=data)
        self.participants: Optional[List[str]] = [data.get('participants', None)]
