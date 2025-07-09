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

from __future__ import annotations

from teamly.abc import ChannelType

from .types.channel import BaseChannelPayload, VoiceChannelPayload, WatchstreamChannelPayload
from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ConnectionState


class BaseChannel:

    def __init__(self,*,state: ConnectionState, data: BaseChannelPayload) -> None:
        self.id: str = data['id']
        self.type: str = data['type']
        self.team_id: str = data['teamId']
        self.name: str = data['name']

        self.description: Optional[str] = data.get('description', None)

        self.created_by: str = data['createdBy'] if isinstance(data['createdBy'], str) else data['createdBy']['id']
        self.created_at: str = data['createdAt']

        self.parent_id: Optional[str] = data.get('parentId', None)
        self.priority: int = data['priority']

        self.permissions: Optional[Dict[str,Any]] = data.get('role')


    def __repr__(self) -> str:
        return f"<BaseChannel id={self.id} name={self.name!r} teamId={self.team_id}>"



class VoiceChannel(BaseChannel):

    def __init__(self, *, state: ConnectionState, data: VoiceChannelPayload) -> None:
        super().__init__(state=state, data=data)
        self.participants: Optional[List[str]] = data.get('participants', None)
        self.user_limit: int = data.get('userLimit', None)

    def __repr__(self) -> str:
        return f"<VoiceChannel id={self.id} type={self.type!r} name={self.name!r} teamId={self.team_id}>"

class TextChannel(BaseChannel):

    def __repr__(self) -> str:
        return f"<TextChannel id={self.id} type={self.type!r} name={self.name!r} teamId={self.team_id}>"

class DMChannel:
    pass

class TodoChannel(BaseChannel):

    def __repr__(self) -> str:
        return f"<TodoChannel id={self.id} type{self.type!r} name={self.name!r} teamId={self.team_id}>"

class WatchstreamChannel(BaseChannel):

    def __init__(self, *, state: ConnectionState, data: WatchstreamChannelPayload) -> None:
        super().__init__(state=state, data=data)
        self.additional_data = data.get('additionalData', None)

    def __repr__(self) -> str:
        return (
            f"<WatchsteamChannel id={self.id} type={self.type!r} name={self.name!r} teamId={self.team_id}>\n"
            f"<additionalData={self.additional_data}>"
        )

class AnnouncementChannel(BaseChannel):

    def __repr__(self) -> str:
        return f"<AnnouncementChannel id={self.id} type={self.type!r} name={self.name!r} teamId{self.team_id}>"

def _team_channel_factory(channel_type: str):
    if ChannelType.TEXT == 'text':
        return TextChannel
