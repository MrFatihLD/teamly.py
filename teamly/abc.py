


from enum import Enum


class ChannelType(Enum):
    TEXT = 'text'
    VOICE = 'voice'
    TODO = 'todo'
    WATCHSTREAM = 'watchstream'
    ANNOUNCEMENT = 'announcement'

    def __str__(self) -> str:
        return self.value

class Status(Enum):
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2
    DO_DO_DISTURB = 3
