
from __future__ import annotations

from .types.webhook import Webhook as WebhookPayload

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .state import ConnectionState

class Webhook:

    def __init__(self, state: ConnectionState, data: WebhookPayload) -> None:
        self.id: str = data['id']
        self.channel_id: str = data['channelId']
        self.team_id: str = data['teamId']
        self.username: str = data['username']
        self.profile_picture: Optional[str] = data.get('profilePicture', None)
        self.token: str = data['token']
        self.created_by: str = data['createdBy']
        self.created_at: str = data['createdAt']
        self.updated_at: str = data['updatedAt']

    def __repr__(self) -> str:
        return (
            f"<Webhook id={self.id} username={self.username} token={self.token}>\n"
            f"<channelId={self.channel_id} teamId={self.team_id}>"
        )
