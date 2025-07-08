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

from .types.user import UserBadgeProxy, UserPayload, UserRPCProxy, UserStatusProxy
from .utils import Status
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ConnectionState

class _UserTag:
    id: str

class UserStatus:
    def __init__(self, data: UserStatusProxy) -> None:
        self.content: Optional[str] = data.get('content', None)
        self.emoji_id: Optional[str] = data.get('emojiId', None)

class UserRPC:
    def __init__(self, data: UserRPCProxy) -> None:
        self.type: Optional[str] = data.get('type', None)
        self.name: Optional[str] = data.get('name', None)
        self.id: Optional[int] = data.get('id', None)
        self.started_id: Optional[str] = data.get('startedAt', None)

class Badge:
    def __init__(self, data: UserBadgeProxy) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.icon: str = data['icon']

class BaseUser(_UserTag):
    def __init__(self,*, state: ConnectionState, data: UserPayload) -> None:
        self.id: str = data['id']
        self.username: str = data['username']
        self.subdomain: str = data['subdomain']

        self.profile_picture: Optional[str] = data.get('profilePicture', None)
        self.banner: Optional[str] = data.get('banner', None)

        self.bot: bool = data.get('bot', False)
        self.system: bool = data.get('system', False)
        self.presence: Status = data.get('presence', 0)

        self.flags: Optional[str] = data.get('flags', None)

        self.badges: List[Badge] = [
            Badge(b) for b in data.get('badges', None)
        ]

        self.user_status: Optional[UserStatus] = (
            UserStatus(data.get('userStatus', None))
        )

        self.user_rpc: Optional[UserRPC] = (
            UserRPC(data.get('userRPC', None))
        )

        self.connections: List = data.get('connections', [])

        self.created_at: Optional[str] = data['createdAt']


    def __repr__(self) -> str:
        return (
            f"<BaseUser id={self.id} username={self.username!r} subdomain={self.subdomain!r}> "
            f"<bot={self.bot}>"
        )

    def __eq__(self, other: object, /) -> bool:
        return isinstance(other, _UserTag) and other.id == self.id

class ClientUser(BaseUser):

    def __init__(self,*, state: ConnectionState, data: UserPayload) -> None:
        super().__init__(state=state,data=data)

    def __repr__(self) -> str:
        return (
            f"<ClientUser id={self.id} name={self.username!r} subdomain={self.subdomain!r}> "
            f"<bot={self.bot}>"
        )

class User(BaseUser):

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} subdomain={self.subdomain!r}>"
