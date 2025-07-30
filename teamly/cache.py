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

import asyncio
from collections import OrderedDict
import json
from typing import Dict, Optional, Union, Any, TYPE_CHECKING

from loguru import logger
from .utils import MISSING

from .channel import TextChannel, VoiceChannel, _channel_factory
from .http import HTTPClient
from .message import Message
from .team import Team
from .member import Member
from .user import ClientUser

if TYPE_CHECKING:
    from .state import ConnectionState
    from .channel import (
        TextChannel,
        VoiceChannel
    )
    from .message import Message

    MessageAbleChannel = Union[TextChannel]
    Channel = Union[TextChannel, VoiceChannel]

__all__ = [
    "Cache"
]

class Cache:

    def __init__(self, state: ConnectionState) -> None:
        self._state: ConnectionState = state
        self._http: HTTPClient = self._state.http
        self.maxLength: int = 100
        self.clear()

    def clear(self):
        self._user: Optional[ClientUser] = None
        self._teams: Dict[str, Team] = {}
        self._channels: Dict[str, Dict[str, Channel]] = {}
        self._messages: Dict[str, Dict[str, OrderedDict[str, Message]]] = OrderedDict()
        self._members: Dict[str, Dict[str, Member]] = {}

    async def setup_cache(self, data: Any):
        #get ClietnUser Payload
        self._user = ClientUser(state=self._state, data=data['user'])
        logger.info(f"Bot connected as {self._user.username!r}")
        await self.__fetch_teams(data['teams'])
        tasks = []
        for team in self._teams:
            tasks.append(self.__fetch_channels(team))
            tasks.append(self.__fetch_team_members(team))

        await asyncio.gather(*tasks)

    async def __fetch_teams(self, teams: Dict[str, Any]):
        for team in teams:
            self._teams[team['id']] = Team(state=self._state, data=team)

    async def __fetch_channels(self, teamId: str):
        channels = await self._http.get_channels(teamId)
        channels = json.loads(channels)

        for data in channels['channels']:
            factory = _channel_factory(data['type'])
            channel: Channel = MISSING
            team: Team = MISSING

            if teamId not in self._channels:
                self._channels[teamId] = {}

            if factory:
                team = self._teams[teamId]
                self._channels[teamId][data['id']] = channel = factory(state=self._state,team=team, data=data)

            if teamId not in self._messages:
                self._messages[teamId] = OrderedDict()

            if data['type'] == 'text':
                self._messages[teamId][channel.id] = await self.__fetch_channel_messages(channel=channel)

    async def __fetch_channel_messages(self, channel: MessageAbleChannel, limit: int = 1000):
        try:
            cache: OrderedDict[str,Member] = OrderedDict()
            remaining = limit
            offset = 0

            while remaining > 0:
                fetch_count = min(50, remaining)

                response = await self._http.get_channel_messages(
                    channelId=channel.id, offset=offset, limit=fetch_count
                )
                data = json.loads(response)
                messages = data.get("messages",[])

                for message in messages:
                    if message.get("replyTo") is not None:
                        message["replyTo"] = next(
                            (
                                reply
                                for reply in data.get("replyMessages", [])
                                if reply["id"] == message["replyTo"]
                            ),
                            message["replyTo"]
                        )

                    cache[message["id"]] = Message(
                        state=self._state, channel=channel, data=message
                    )

                count = len(messages)
                remaining -= count
                offset += count

                if count < fetch_count:
                    break

            return cache
        except Exception as e:
            logger.error(f"Exception error: {e}")




    async def __fetch_team_members(self, teamId: str):
        members = await self._http.get_member(teamId, "")
        members = json.loads(members)

        if teamId not in self._members:
            self._members[teamId] = {}

        for member in members['members']:
            if member['id'] not in self._members[teamId]:
                self._members[teamId][member['id']] = Member(state=self._state, data=member)


    #Team Cache
    def get_team(self, teamId: str):
        if teamId in self._teams:
            return self._teams[teamId]
        else:
            return "..."

    def update_team(self, teamId: str, updated_team: str):
        if teamId in self._teams:
            self._teams[teamId] = updated_team


    #Channel Cache
    def add_channel(self, teamId: str, channelId: str, channel: MessageAbleChannel):
        if teamId not in self._channels:
            self._channels[teamId] = {}

        if channelId not in self._channels[teamId]:
            self._channels[teamId][channelId] = channel
            logger.opt(colors=True).debug(f"<cyan>Added channel {channelId!r} to cache successfuly</cyan>")

    def delete_channel(self, teamId: str, channelId: str):
        if channelId in self._channels[teamId]:
            self._channels[teamId].pop(channelId)
            logger.opt(colors=True).debug(f"<cyan>Deleted channel {channelId!r} from cache successfuly</cyan>")

    def update_channel(self, teamId: str, channelId: str, channel: MessageAbleChannel):
        if channelId in self._channels[teamId]:
            self._channels[teamId][channelId] = channel
            logger.opt(colors=True).debug(f"<cyan>Updated channel {channelId!r} from cache successfuly</cyan>")

    def get_channel(self, teamId: str, channelId: str) -> Channel | None:
        if channelId in self._channels[teamId]:
            return self._channels[teamId][channelId]

    def get_channels(self, teamId: str) -> Dict[str, Channel]:
            return self._channels[teamId]

    #Voice Channel
    def voice_participants_joined(self,teamId: str, channelId: str, participantId: str):
        if self._channels[teamId][channelId]:
            voice = self._channels[teamId][channelId]
            if not any(p.get('id') == participantId for p in voice._participants):
                voice._participants.append({"id": participantId})

    def voice_participants_leaved(self, teamId:str, channelId: str, participantId: str):
        if self._channels[teamId][channelId]:
            voice = self._channels[teamId][channelId]
            for par in voice._participants:
                if par.get('id') == participantId:
                    voice._participants.remove({"id": participantId})


    #Message Cache

    async def get_message(self, teamId: str, channelId: str, messageId: str):
        if teamId in self._messages:
            if channelId in self._channels[teamId]:
                if self._messages[teamId][channelId][messageId]:
                    return self._messages[teamId][channelId][messageId]
                else:
                    message = await self._state.http.get_channel_message_by_id(channelId=channelId, messageId=messageId)
                    channel = self.get_channel(teamId=teamId, channelId=channelId)
                    return Message(state=self._state, channel=channel, data=message)

    async def get_messages(self,channelId: str,offset: int = 0, limit: int = 130):
        pass

    def add_message(self, teamId: str, channelId: str, message: Message):
        if channelId in self._messages[teamId]:
            self._messages[teamId][channelId][message.id] = message

        if len(self._messages[teamId][channelId]) > self.maxLength:
            self._messages[teamId][channelId].popitem(last=False)

    def update_message(self, teamId: str, channelId: str, message: Message):
        if channelId in self._messages[teamId]:
            if message.id in self._messages[teamId][channelId]:
                upt_message = self._messages[teamId][channelId][message.id]
                self._messages[teamId][channelId][message.id] = message
                return upt_message

    def delete_message(self, teamId: str, channelId: str, messageId: str):
        if channelId in self._messages[teamId]:
            if messageId in self._messages[channelId][messageId]:
                message = self._messages[teamId][channelId].pop(messageId)
                logger.opt(colors=True).debug(f"<cyan>deleted channel message {messageId!r} from cache successfuly</cyan>")
                return message



    #Member

    def get_members(self, teamId: str) -> Dict[str, Member]:
        return self._members[teamId]

    def get_member(self, teamId: str, userId: str):
        return self._members[teamId][userId] if userId in self._members[teamId] else None

    def add_member(self, teamId: str, member: Member):
        if member.id not in self._members[teamId]:
            self._members[teamId][member.id] = member

    def delete_member(self, teamId: str, memberId: str):
        if memberId in self._members[teamId]:
            self._members[teamId].pop(memberId)
