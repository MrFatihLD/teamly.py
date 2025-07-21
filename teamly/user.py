
from __future__ import annotations


from teamly.abc import StatusLiteral
from .types.user import User as UserPayload
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .state import ConnectionState

__all__ = (
    "ClientUser",
    "User"
)

class _UserTag:
    __slots__ = ()
    id: str

class BaseUser(_UserTag):

    def __init__(self,*, state: ConnectionState, data: UserPayload) -> None:
        self._state = state
        self._update(data)

    def _update(self, data: UserPayload):
        self.id: str = data['id']
        self.username: str = data['username']
        self.subdomain: str = data.get('subdomain')
        self.profile_picture: Optional[str] = data.get('profilePicture', None)
        self.banner: Optional[str] = data.get('banner', None)

        self.bot: bool = data['bot']
        self.presence: StatusLiteral = data.get('presence', 0)
        self.flags: str = data['flags']
        self.badges: List[Dict[str,Any]] = data['badges']
        self._user_status: Optional[Dict[str,Any]] = data.get('userStatus', None)
        self.user_rpc: Optional[Dict[str,Any]] = data.get('userRPC', None)
        self.connections: List[str] = data.get('connections', [])
        self.created_at: str = data['createdAt']
        self.system: bool = data.get('system', False)

    def __repr__(self) -> str:
        return (
            f"<BaseUser id={self.id} username={self.username} subdomain={self.subdomain} "
            f"bot={self.bot} system={self.system}>"
        )

    def __eq__(self, other: object, /) -> bool:
        return isinstance(other, _UserTag) and self.id == other.id


class ClientUser(BaseUser):

    def __init__(self, *, state: ConnectionState, data: UserPayload) -> None:
        super().__init__(state=state, data=data)

    def _update(self, data: UserPayload):
        super()._update(data)

        self.verified: bool = data.get('verified', False)
        self.disabled: bool = data.get('disabled', False)
        self.last_online: str = data.get('lastOnline', None)

    def __repr__(self) -> str:
        return (
            f"<ClientUser id={self.id} username={self.username} subdoamin={self.subdomain} "
            f"bot={self.bot} system={self.system}>"
        )

class User(BaseUser):

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} username={self.username} subdomain={self.subdomain} "
            f"bot={self.bot} system={self.system}>"
        )
