

from __future__ import annotations


from .channel import TextChannel
from enum import Enum
from typing import Union, Literal



class ChannelType(str, Enum):
    TEXT = 'text'
    VOICE = 'voice'
    TODO = 'todo'
    WATCHSTREAM = 'watchstream'
    ANNOUNCEMENT = 'announcement'

    def __str__(self) -> str:
        return self.value

MessageAbleChannel = Union[TextChannel]


class Status(int,Enum):
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2
    DO_DO_DISTURB = 3

StatusLiteral = Literal[Status.OFFLINE, Status.ONLINE, Status.IDLE, Status.DO_DO_DISTURB]
