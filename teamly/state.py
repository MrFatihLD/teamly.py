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

import asyncio
import inspect
import json

from asyncio.unix_events import logger

from teamly.abc import MessageAbleChannel
from teamly.reaction import Reaction
from teamly.todo import TodoItem






from .message import Message
from .member import Member
from .team import Team
from .channel import TextChannel, VoiceChannel, _channel_factory
from .user import ClientUser, User
from .http import HTTPClient
from typing import Dict, Callable, Any,  Optional, Union


class ConnectionState:

    def __init__(self, dispatch: Callable[...,Any],http: HTTPClient) -> None:
        self.http: HTTPClient = http
        self.dispatch: Callable[...,Any] = dispatch

        self.parsers: Dict[str, Callable[[Any], None]]
        self.parsers = parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith('parse_'):
                parsers[attr[6:].upper()] = func

        self.clear()

    def clear(self):
        self._user: Optional[ClientUser] = None
        self._teams: Dict[str, Team] = {}
        self._channels: Dict[str, Dict[str, Union[TextChannel,VoiceChannel]]] = {}
        self._messages: Dict[str, Dict[str, Dict[str, Message]]] = {}
        self._users: Dict[str,Member] = {}


    def parse_ready(self, data: Any):
        self._user = ClientUser(state=self, data=data['user'])
        self._teams = {team['id']: Team(state=self,data=team) for team in data['teams']}
        for team in self._teams:
            asyncio.create_task(self._get_channels(team))
            asyncio.create_task(self.get_members(team))
        self.dispatch("ready")

    async def _get_channels(self, teamId: str):
        channels = await self.http.get_channels(teamId)
        channels = json.loads(channels)
        for channel in channels['channels']:
            factory = _channel_factory(channel['type'])

            if teamId not in self._channels:
                self._channels[teamId] = {}

            if factory:
                self._channels[teamId][channel['id']] = factory(state=self, data=channel)

            if teamId not in self._messages:
                self._messages[teamId] = {}

            if channel['type'] == 'text':
                self._messages[teamId][channel['id']] = await self._get_cach_messages(channelId=channel['id'])

    def get_channel(self, teamId: str, channelId: str) -> MessageAbleChannel:
        return self._channels[teamId][channelId]

    async def _get_cach_messages(self, channelId: str):
        try:
            messages = await self.http.get_channel_messages(channelId=channelId, limit=50)
            messages = json.loads(messages)
            temp_dict = {}

            if messages['messages']:
                for message in messages['messages']:
                    temp_dict[message['id']] = Message(state=self, data=message)

            if messages['replyMessages']:
                for message in messages['replyMessages']:
                    temp_dict[message['id']] = Message(state=self, data=message)

            return temp_dict
        except Exception as e:
            logger.error(f"Exception error: {e}")
            return {}

    async def get_members(self, teamId: str):
        members = await self.http.get_member(teamId,"")
        members = json.loads(members)
        for member in members['members']:
            if member['id'] not in self._users:
                self._users[member['id']] = User(state=self, data=member)

    def parse_channel_created(self, data: Dict[str,Any]):
        factory = _channel_factory(data['channel']['type'])
        if factory:
            channel = factory(state=self, data=data['channel'])
            self.dispatch('channel_created', channel)

    def parse_channel_deleted(self, data: Any):
        self.dispatch('channel_deleted',data)

    def parse_channel_updated(self, data: Any):
        factory = _channel_factory(data['channel']['type'])
        if factory:
            channel = factory(state=self, data=data)
            self.dispatch('channel_updated', channel)



    def parse_message_send(self, data: Any):
        message = Message(state=self, data=data['message'])
        self.dispatch("message",message)

    def parse_message_updated(self, data: Any):
        message = Message(state=self, data=data['message'])
        self.dispatch("message_updated", message)

    def parse_message_deleted(self, data: Any):
        self.dispatch("message_deleted", data)

    def parse_message_reaction_added(self, data: Any):
        channel = self.get_channel(data['teamId'],data['channelId'])
        reaction = Reaction(state=self, channel=channel, data=data)
        self.dispatch("message_reaction", reaction)

    def parse_message_reaction_removed(self, data: Any):
        channel = self.get_channel(data['teamId'],data['channelId'])
        reaction = Reaction(state=self, channel=channel, data=data)
        self.dispatch("message_reaction_removed", reaction)



    def parse_presence_update(self, data: Any):
        self.dispatch("presence_updated",data)



    def parse_team_role_created(self, data: Any):
        self.dispatch("team_role", data)

    def parse_team_role_deleted(self, data: Any):
        self.dispatch("team_role_deleted", data)

    def parse_team_roles_updated(self, data: Any):
        self.dispatch("team_roles_updated", data)

    def parse_team_updated(self, data: Any):
        self.dispatch("team_updated", data)



    def parse_todo_item_created(self, data: Any):
        todo_item = TodoItem(state=self, data=data)
        self.dispatch("todo_item", todo_item)
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_todo_item_deleted(self, data: Any):
        self.dispatch("todo_item_deleted", data)

    def parse_todo_item_updated(self, data: Any):
        todo_item = TodoItem(state=self, data=data)
        self.dispatch("todo_item_updated", todo_item)




    def parse_user_joined_team(self, data: Any):
        self.dispatch("user_joined_team")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_left_team(self, data: Any):
        self.dispatch("user_left_team")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_joined_voice_channel(self, data: Any):
        self.dispatch("user_joinded_voice_channel")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_left_voice_channel(self, data: Any):
        self.dispatch("user_left_voice_channel")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_profile_updated(self, data: Any):
        self.dispatch("user_profile_updated")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_role_added(self, data: Any):
        self.dispatch("user_role_added")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_role_removed(self, data: Any):
        self.dispatch("user_role_removed")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_updated_voice_metadata(self, data: Any):
        self.dispatch("user_updated_voice_metadata")
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_blog_created(self, data: Any):
        self.dispatch("blog")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_blog_deleted(self, data: Any):
        self.dispatch("blog_deleted")
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_categories_priority_updated(self, data: Any):
        self.dispatch("categories_priority_updated")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_category_updated(self, data: Any):
        self.dispatch("category_updated")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_category_deleted(self, data: Any):
        self.dispatch("category_deleted")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_category_created(self, data: Any):
        self.dispatch("category")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_channels_priority_updated(self, data: Any):
        self.dispatch("channels_priority_updated")
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_announcement_created(self, data: Any):
        self.dispatch("announcement")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_announcement_deleted(self, data: Any):
        self.dispatch("announcement_deleted")
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_application_created(self, data: Any):
        self.dispatch("application")
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_application_updated(self, data: Any):
        self.dispatch("application_updated")
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_voice_channel_move(self, data: Any):
        self.dispatch("voice_channel_move")
        print(json.dumps(data,indent=4, ensure_ascii=False))
