
import inspect
import json

from .http import HTTPClient
from .message import Message
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

    # def clean(self):
    #     self._user = Optional[User]

    def parse_ready(self, data: Any):
        self.dispatch("ready")
        print(json.dumps(data['user'],indent=4))

    def parse_message_send(self, data: Any):
        message = Message(state=self,data=data['message'])
        self.dispatch("message",message)
        print(json.dumps(data['message'],indent=4))
