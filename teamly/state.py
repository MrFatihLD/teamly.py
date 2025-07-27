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

from loguru import logger

from teamly.reaction import Reaction

from .user import ClientUser
from .team import Team
from .role import Role
from .announcement import Announcement
from .application import Application
from .member import Member
from .message import Message
from .cache import Cache
from .todo import TodoItem
from .channel import _channel_factory
from .blog import Blog
from .http import HTTPClient

from typing import Dict, Callable, Any, Optional


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
        self.cache: Cache = Cache(state=self)

    async def __setup_before_ready(self, data: Any):
        await asyncio.wait_for(self.cache.setup_cache(data=data), timeout=15)
        self._user = self.cache._user
        self.dispatch('ready')

    def parse_ready(self, data: Any):
        logger.info("Bot connected successfuly")
        asyncio.create_task(self.__setup_before_ready(data), name = "setup_ready")




    def parse_channel_created(self, data: Dict[str,Any]):
        factory = _channel_factory(data['channel']['type'])
        team = self.cache.get_team(teamId=data['teamId'])
        if factory:
            channel = factory(state=self,team=team, data=data['channel'])
            self.cache.add_channel(teamId=channel.team_id, channelId=channel.id, channel=channel)
            self.dispatch('channel_created', channel)

    def parse_channel_deleted(self, data: Any):
        self.cache.delete_channel(teamId=data['teamId'], channelId=data['channelId'])
        self.dispatch('channel_deleted',data)

    def parse_channel_updated(self, data: Any):
        factory = _channel_factory(data['channel']['type'])
        team = self.cache.get_team(teamId=data['teamId'])
        if factory:
            channel = factory(state=self,team=team, data=data['channel'])
            self.cache.update_channel(teamId=channel.team_id, channelId=channel.id, channel=channel)
            self.dispatch('channel_updated', channel)



    def parse_message_send(self, data: Any):
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        message = Message(state=self, channel=channel, data=data['message'])
        self.dispatch("message",message)

    def parse_message_updated(self, data: Any):
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        message = Message(state=self,channel=channel,data=data['message'])
        upt_msg = self.cache.update_message(teamId=data['teamId'], channelId=data['channelId'], message=message) #noqa -> type: ignore
        self.dispatch("message_updated", message)

    def parse_message_deleted(self, data: Any):
        message = self.cache.delete_message(teamId=data['teamId'], channelId=data['channelId'], messageId=data['messageId'])
        self.dispatch("message_deleted", message)

    def parse_message_reaction_added(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        message = self.cache.get_message(teamId=data['teamId'], channelId=data['channelId'], messageId=data['messageId'])
        reaction = Reaction(state=self, team=team, channel=channel, message=message, data=data)
        self.dispatch("message_reaction", reaction)

    def parse_message_reaction_removed(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        message = self.cache.get_message(teamId=data['teamId'], channelId=data['channelId'], messageId=data['messageId'])
        reaction = Reaction(state=self, team=team, channel=channel, message=message, data=data)
        self.dispatch("message_reaction_removed", reaction)



    def parse_presence_update(self, data: Any):
        self.dispatch("presence_updated",data)



    def parse_team_role_created(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        if team:
            role = Role(state=self,team=team,data=data['role'])
            self.dispatch("team_role", role)

    def parse_team_role_deleted(self, data: Any):
        self.dispatch("team_role_deleted", data)

    def parse_team_roles_updated(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        if team:
            roles = [Role(state=self,team=team,data=role) for role in data['roles']]
            self.dispatch("team_roles_updated", roles)

    def parse_team_updated(self, data: Any):
        team = Team(state=self,data=data['team'])
        self.cache.update_team(teamId=data['team']['id'], updated_team=team)
        self.dispatch("team_updated", team)



    def parse_todo_item_created(self, data: Any):
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        todo_item = TodoItem(state=self,channel=channel, data=data['todo'])
        self.dispatch("todo_item", todo_item)
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_todo_item_deleted(self, data: Any):
        self.dispatch("todo_item_deleted", data)

    def parse_todo_item_updated(self, data: Any):
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        todo_item = TodoItem(state=self,channel=channel, data=data)
        self.dispatch("todo_item_updated", todo_item)




    def parse_user_joined_team(self, data: Any):
        member = Member._new_member(state=self, data=data['user'], teamId=data['teamId'])
        self.cache.add_member(teamId=data['teamId'], member=member)
        self.dispatch("user_joined_team")
        print('parse_user_joined_team')
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_left_team(self, data: Any):
        self.cache.delete_member(teamId=data['teamId'], memberId=data['member']['id'])
        self.dispatch("user_left_team")
        print(json.dumps(data,indent=4, ensure_ascii=False))


    def parse_user_joined_voice_channel(self, data: Any):
        print(data)
        self.cache.voice_participants_joined(teamId=data['teamId'], channelId=data['channelId'],participantId=data['user']['id'])
        voice = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        self.dispatch("user_joinded_voice_channel",voice)

    def parse_user_left_voice_channel(self, data: Any):
        self.cache.voice_participants_leaved(teamId=data['teamId'], channelId=data['channelId'],participantId=data['user']['id'])
        voice = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        self.dispatch("user_left_voice_channel", voice)


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
        print(data)
        self.dispatch("user_updated_voice_metadata")




    def parse_blog_created(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        blog = Blog(state=self,team=team, data=data)
        self.dispatch("blog", blog)

    def parse_blog_deleted(self, data: Any):
        self.dispatch("blog_deleted", data)




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
        channel = self.cache.get_channel(teamId=data['teamId'], channelId=data['channelId'])
        announcement = Announcement(state=self,channel=channel, data=data['announcement'])
        self.dispatch("announcement",announcement)

    def parse_announcement_deleted(self, data: Any):
        self.dispatch("announcement_deleted",data)




    def parse_application_created(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        if team:
            app = Application(state=self,team=team,data=data)
            self.dispatch("application", app)

    def parse_application_updated(self, data: Any):
        team = self.cache.get_team(teamId=data['teamId'])
        if team:
            app = Application(state=self,team=team,data=data['application'])
            self.dispatch("application_updated", app)




    def parse_voice_channel_move(self, data: Any):
        self.dispatch("voice_channel_move",data)
        print(json.dumps(data,indent=4, ensure_ascii=False))
