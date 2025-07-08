

from __future__ import annotations

from .types.role import RolePayload

from typing import TYPE_CHECKING, Optional, Dict

if TYPE_CHECKING:
    from .state import ConnectionState


class Role:

    def __init__(self,*, state: ConnectionState, data: RolePayload) -> None:
        self.id: str = data['id']
        self.team_id: str = data['teamId']
        self.name: str = data['name']
        self.icon_url: Optional[str] = data.get('iconUrl', None)
        self.color: str = data['color']
        self.color2: str = data.get('color2', None)
        self.permissions: int = data['permissions']
        self.priority: int = data.get('priority', 0)
        self.created_at: str = data['createdAt']
        self.update_at: Optional[str] = data.get('updatedAt', None)
        self.is_displayed_separately: bool = data.get('isDisplayedSeparately', True)
        self.is_self_assignable: Optional[bool] = data.get('isSelfAssignable', False)
        self.icon_emoji_id: Optional[str] = data.get('iconEmojiId', None)
        self.mentionable: bool = data.get('mentionable', True)
        self.botScope: Dict[str, Optional[str]] = data.get('botScope', {})

    def __repr__(self) -> str:
            return f"<Role id={self.id} name={self.name} team_id={self.team_id}>"
