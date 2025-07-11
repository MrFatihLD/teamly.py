
from __future__ import annotations

from loguru import logger

from teamly.abc import ChannelType


from .types.channel import TextChannelPayload, VoiceChannelPayload
from typing import TYPE_CHECKING, Dict, Any, List, Optional

if TYPE_CHECKING:
    from .state import ConnectionState


class TextChannel:

    def __init__(self,*, state: ConnectionState, data: TextChannelPayload) -> None:
        self._state = state
        self._update(data)

    def _update(self, data: TextChannelPayload):
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']

        self.description: Optional[str] = data.get('description', None)
        self.created_by: str = data['createdBy']
        self.parent_id: Optional[str] = data.get('parentId', None)
        self.priority: int = data['priority']
        self.rate_limit_per_user: int = data['rateLimitPerUser']
        self.created_at: str = data['createdAt']
        self.permissions: Dict[str,Any] = data['permissions'].get('role', {})
        self.additional_data: Dict[str,Any] = data.get('additionalData', {})

    def __repr__(self) -> str:
        return f"<TextChannel id={self.id} type={self.type} teamId={self.team_id} name={self.name}>"

    async def fetch_messages(self, offset: int = 0, limit: int = 15):
        try:
            offset = str(offset)
            limit = str(limit)

            return await self._state.http.get_channel_messages(self.id, offset, limit)
        except TypeError as e:
            logger.error("TypeError {}", e)

    async def delete_message(self, messageId: str):
        return await self._state.http.delete_message(self.id, messageId)

    async def react_message(self, messageId: str, emojiId: str):
        return await self._state.http.react_to_message(self.id, messageId, emojiId)

    async def edit(self, name: str, description: str = None):
        if len(name) < 1 and len(name) > 20:
            raise ValueError('\'name\' must be 1<= n <=20')

        payload = {
            "name": name,
            "description": description
        }

        return await self._state.http.update_channel(self.team_id, self.id, payload)




class VoiceChannel:

    def __init__(self,*, state: ConnectionState, data: VoiceChannelPayload) -> None:
        self._state = state
        self._update(data)

    def _update(self, data: VoiceChannelPayload):
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']

        self.description: Optional[str] = data.get('description', None)
        self.created_by: str = data['createdBy']
        self.parent_id: Optional[str] = data.get('parentId', None)
        self.priority: int = data['priority']
        self.participants: List[str] = data.get('participants', [])
        self.created_at: str = data['createdAt']
        self.permissions: Dict[str,Any] = data['permissions'].get('role', {})
        self.additional_data: Dict[str,Any] = data.get('additionalData', {})

    def __repr__(self) -> str:
        return f"<VoiceChannel id={self.id} type={self.type} teamId={self.team_id} name={self.name}>"


@staticmethod
def _channel_factory(type: str):
    if ChannelType.TEXT == type:
        return TextChannel
    elif ChannelType.VOICE == type:
        return VoiceChannel
    else:
        return None
