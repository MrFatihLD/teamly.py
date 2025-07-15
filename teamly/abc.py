
from __future__ import annotations

from enum import Enum
from typing import Literal, TYPE_CHECKING, Union


if TYPE_CHECKING:
    pass

class ChannelType(str, Enum):
    TEXT = 'text'
    VOICE = 'voice'
    TODO = 'todo'
    WATCHSTREAM = 'watchstream'
    ANNOUNCEMENT = 'announcement'

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Status(int,Enum):
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2
    DO_DO_DISTURB = 3

StatusLiteral = Literal[Status.OFFLINE, Status.ONLINE, Status.IDLE, Status.DO_DO_DISTURB]



class MessageAble:

    def send(
        self,
        content: str,
        *,
        embed: str
    ):
        pass
