
from __future__ import annotations

import asyncio
import json
from typing import Dict, Optional, Union, Any, TYPE_CHECKING

from loguru import logger

from teamly.abc import MessageAbleChannel
from teamly.channel import TextChannel, VoiceChannel, _channel_factory
from teamly.http import HTTPClient
from teamly.message import Message
from teamly.team import Team
from teamly.member import Member
from teamly.user import ClientUser

if TYPE_CHECKING:
    from teamly.state import ConnectionState

class Cache:

    def __init__(self, state: ConnectionState) -> None:
        self._state: ConnectionState = state
        self._http: HTTPClient = self._state.http
        self.clear()

    def clear(self):
        self._user: Optional[ClientUser] = None
        self._teams: Dict[str, Team] = {}
        self._channels: Dict[str, Dict[str, Union[TextChannel, VoiceChannel]]] = {}
        self._messages: Dict[str, Dict[str, Dict[str, Message]]] = {}
        self._members: Dict[str, Dict[str, Member]] = {}

    async def setup_cache(self, data: Any):
        #get ClietnUser Payload
        self._user = ClientUser(state=self._state, data=data['user'])
        logger.info(f"Bot connected as {self._user.username!r}")
        await self._fetch_teams(data['teams'])
        for team in self._teams:
            asyncio.create_task(self._fetch_channels(team))
            asyncio.create_task(self._fetch_team_members(team))

    async def _fetch_teams(self, teams: Dict[str, Any]):
        for team in teams:
            self._teams[team['id']] = Team(state=self._state, data=team)

    async def _fetch_channels(self, teamId: str):
        channels = await self._http.get_channels(teamId)
        channels = json.loads(channels)

        for data in channels['channels']:
            factory = _channel_factory(data['type'])
            channel: MessageAbleChannel = None

            if teamId not in self._channels:
                self._channels[teamId] = {}

            if factory:
                self._channels[teamId][data['id']] = channel = factory(state=self._state, data=data)

            if teamId not in self._messages:
                self._messages[teamId] = {}

            if data['type'] == 'text':
                self._messages[teamId][channel.id] = await self._fetch_channel_messages(channel=channel)

    async def _fetch_channel_messages(self, channel: MessageAbleChannel):
        try:
            messages = await self._http.get_channel_messages(channelId=channel.id, limit=50)
            messages = json.loads(messages)

            message_dict = {}

            if messages['messages']:
                for message in messages['messages']:
                    message_dict[message['id']] = Message(state=self._state, channel=channel, data=message)

            if messages['replyMessages']:
                for message in messages['replyMessages']:
                    message_dict[message['id']] = Message(state=self._state, channel=channel, data=message)

            return message_dict
        except Exception as e:
            logger.error(f"Exception error: {e}")
            return {}

    async def _fetch_team_members(self, teamId: str):
        members = await self._http.get_member(teamId, "")
        members = json.loads(members)

        if teamId not in self._members:
            self._members[teamId] = {}

        for member in members['members']:
            if member['id'] not in self._members:
                self._members[member['id']] = Member(state=self._state, data=member)
