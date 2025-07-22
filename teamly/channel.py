
from __future__ import annotations


from teamly.abc import MessageAble

from .enums import ChannelType

from .types.channel import TextChannelPayload, VoiceChannelPayload, BaseChannel as BaseChannelPayload
from typing import TYPE_CHECKING, Dict, Any, List, Mapping, Optional

if TYPE_CHECKING:
    from .state import ConnectionState

class BaseChannel:

    def __init__(self,*, state: ConnectionState, data: BaseChannelPayload) -> None:
        self._state: ConnectionState = state
        self._update(data)

    def _update(self, data: Mapping):
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']

        self.description: Optional[str] = data.get('description', None)
        self.created_by: str = data.get('createdBy')
        self.parent_id: Optional[str] = data.get('parentId', None)
        self.priority: int = data['priority']
        self.created_at: str = data['createdAt']
        self.permissions: Dict[str,Any] = data['permissions'].get('role', {})
        self.additional_data: Dict[str,Any] = data.get('additionalData', {})

    async def edit(self, name: str, description: str = None):
        if len(name) < 1 and len(name) > 20:
            raise ValueError('\'name\' must be 1<= n <=20')

        payload = {
            "name": name,
            "description": description
        }

        return await self._state.http.update_channel(self.team_id, self.id, payload)

    def __repr__(self) -> str:
        return f"<BaseChannel id={self.id} name={self.name!r} type={self.type} teamId={self.team_id}>"




class TextChannel(BaseChannel, MessageAble):

    def __init__(self, *, state: ConnectionState, data: TextChannelPayload) -> None:
        super().__init__(state=state, data=data)

    def _update(self, data: Mapping):
        super()._update(data)
        self.rate_limit_per_user: int = data['rateLimitPerUser']

    def __repr__(self) -> str:
        return f"<TextChannel id={self.id} name={self.name!r} type={self.type} teamId={self.team_id}>"

    async def delete_message(self, messageId: str):
        return await self._state.http.delete_message(self.id, messageId)

    async def react_message(self, messageId: str, emojiId: str):
        return await self._state.http.react_to_message(self.id, messageId, emojiId)




class VoiceChannel(BaseChannel):

    def __init__(self, *, state: ConnectionState, data: VoiceChannelPayload) -> None:
        super().__init__(state=state, data=data)

    def _update(self, data: Mapping):
        super()._update(data)
        self.participants: List[str] = data.get('participants', [])

    def __repr__(self) -> str:
        return f"<VoiceChannel id={self.id} name={self.name!r} type={self.type} teamId={self.team_id}>"


class AnnouncementChannel(BaseChannel):

    def __repr__(self) -> str:
        return f"<VoiceChannel id={self.id} name={self.name!r} type={self.type} teamId={self.team_id}>"


@staticmethod
def _channel_factory(type: str):
    if ChannelType.TEXT == type:
        return TextChannel
    elif ChannelType.VOICE == type:
        return VoiceChannel
    elif ChannelType.ANNOUNCEMENT == type:
        return AnnouncementChannel
    else:
        return None
