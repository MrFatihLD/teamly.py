

from __future__ import annotations


from enum import Enum



class ChannelType(str, Enum):
    TEXT = 'text'
    VOICE = 'voice'
    TODO = 'todo'
    WATCHSTREAM = 'watchstream'
    ANNOUNCEMENT = 'announcement'

    def __str__(self) -> str:
        return self.value


class Status(int,Enum):
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2
    DO_DO_DISTURB = 3
