
import inspect
import json

from .http import HTTPClient
from .message import Message
#from .channel import Channel
from typing import Dict, Callable, Any

class ConnectionState:

    def __init__(self, dispatch: Callable[...,Any],http: HTTPClient) -> None:
        self.http: HTTPClient = http
        self.dispatch: Callable[...,Any] = dispatch

        self.parsers: Dict[str, Callable[[Any], None]]
        self.parsers = parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith('parse_'):
                parsers[attr[6:].upper()] = func



    def parse_ready(self, data: Any):
        self.dispatch("ready")
        print(json.dumps(data['user'],indent=4))



    def parse_channel_created(self, data: Dict[str,Any]):
        #channel = Channel(data['channel'])
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_channel_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_channel_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))



    def parse_message_send(self, data: Any):
        message = Message(state=self,data=data['message'])
        self.dispatch("message",message)
        print(json.dumps(data['message'],indent=4))

    def parse_message_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_message_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_message_reaction_added(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_message_reaction_removed(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))



    def parse_presence_update(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))



    def parse_team_role_created(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_team_role_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_team_roles_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_team_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))



    def parse_todo_item_created(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_todo_item_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_todo_item_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_user_joined_team(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_left_team(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_joined_voice_channel(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_left_voice_channel(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_profile_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_role_added(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_role_removed(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_user_updated_voice_metadata(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_blog_created(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_blog_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_categories_priority_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_category_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_category_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_category_created(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_channels_priority_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_announcement_created(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_announcement_deleted(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_application_created(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))

    def parse_application_updated(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))




    def parse_voice_channel_move(self, data: Any):
        print(json.dumps(data,indent=4, ensure_ascii=False))
