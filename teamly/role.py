
from __future__ import annotations
import inspect

from teamly import utils


from .types.role import Role as RolePayload
from typing import TYPE_CHECKING, Dict, Optional, Self

if TYPE_CHECKING:
    from .state import ConnectionState
    from .team import Team

__all__ = ['Role']

class Role:

    __slots__ = (
        '_state',
        'team',
        'id',
        'name',
        '_icon_url',
        'color',
        'color2',
        'permissions',
        '_priority',
        '_created_at',
        '_updated_at',
        'is_displayed_separately',
        'is_self_assignable',
        '_icon_emoji_id',
        'mentionable',
        '_bot_scope'
    )

    def __init__(
        self,
        state: ConnectionState,
        *,
        team: Team,
        data: RolePayload
    ) -> None:
        self._state: ConnectionState = state
        self.team: Team = team

        self.id: str = data['id']
        self.name: str = data['name']

        self._icon_url: Optional[str] = data.get('iconUrl')
        self.color: str = data['color']
        self.color2: Optional[str] = data.get('color2')
        self.permissions: int = data.get('permissions', 0)
        self._priority: int = data.get('priority', 0)
        self._created_at: str = data['createdAt']
        self._updated_at: Optional[str] = data.get('updatedAt')
        self.is_displayed_separately: bool = data.get('isDisplayedSeparately', True)
        self.is_self_assignable: bool = data.get('isSelfAssignable', False)
        self._icon_emoji_id: Optional[str] = data.get('iconEmojiId')
        self.mentionable: bool = data.get('mentionable', True)
        self._bot_scope: Dict[str,str] = data.get('botScope',{})

    @classmethod
    def new(
        cls,
        name: str,
        *,
        permissions: int = 0,
        color: str,
        color2: Optional[str] = None,
        isDisplayedSeparately: Optional[bool] = None
    ) -> Self:
        self = cls.__new__(cls)

        self.name = name
        self.permissions = permissions
        self.color = color
        self.color2 = color2
        self.is_displayed_separately = isDisplayedSeparately

        return self

    def to_dict(self):
        return {
            utils.snake_to_camel(k):v
            for k,v in inspect.getmembers(self, lambda x: not callable(x))
            if not k.startswith('_')
        }

    def __repr__(self) -> str:
        return f"<Role id={self.id} name={self.name} permissions={self.permissions} teamId={self.team.id}>"
