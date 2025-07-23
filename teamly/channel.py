
from __future__ import annotations

import teamly.abc

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




class TextChannel(teamly.abc.MessageAble):

    def __init__(self, *, state: ConnectionState, data: TextChannelPayload) -> None:
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
        self.rate_limit_per_user: int = data['rateLimitPerUser']
        self.created_at: str = data['createdAt']
        self.permissions: Dict[str,Any] = data['permissions'].get('role', {})
        self.additional_data: Dict[str,Any] = data.get('additionalData', {})


    def __repr__(self) -> str:
        return f"<TextChannel id={self.id} name={self.name!r} type={self.type} teamId={self.team_id}>"

    async def delete_message(self, messageId: str):
        return await self._state.http.delete_message(self.id, messageId)

    async def react_message(self, messageId: str, emojiId: str):
        return await self._state.http.react_to_message(self.id, messageId, emojiId)




class VoiceChannel:

    def __init__(self, *, state: ConnectionState, data: VoiceChannelPayload) -> None:
        self._state: ConnectionState = state
        self._update(data)

    def _update(self, data: VoiceChannelPayload):
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']

        self.description: Optional[str] = data.get('description', None)
        self.created_by: str = data.get('createdBy')
        self.parent_id: Optional[str] = data.get('parentId', None)
        self.priority: int = data['priority']
        self._participants: List[Dict[str,str]] = data.get('participants', [])
        self.created_at: str = data['createdAt']
        self.permissions: Dict[str,Any] = data['permissions'].get('role', {})
        self.additional_data: Dict[str,Any] = data.get('additionalData', {})

    @property
    def participants(self):
        return [p.get('id') for p in self._participants if self._participants] if self._participants else []

    def _participant_joined(self, participantId: str):
        if not any(p.get('id') == participantId for p in self._participants):
            self._participants.append({"id": participantId})

    def _participant_leaved(self, participantId: str):
        for par in self._participants:
            if par.get('id') == participantId:
                self._participants.remove({"id": participantId})


    def __repr__(self) -> str:
        return f"<VoiceChannel id={self.id} name={self.name!r} type={self.type} teamId={self.team_id}>"


class AnnouncementChannel:

    def __init__(self, *, state: ConnectionState, data: VoiceChannelPayload) -> None:
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
