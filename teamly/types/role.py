





from typing import TypedDict, Optional


class BotScope(TypedDict):
    userId: Optional[str]


class RolePayload(TypedDict):
    id: str
    teamId: str
    name: str
    iconUrl: Optional[str]
    color: str
    color2: Optional[str]
    permissions: int
    priority: int
    createdAt: str
    updatedAt: Optional[str]
    isDisplayedSeparately: bool
    isSelfAssignable: bool
    iconEmojiId: Optional[str]
    mentionable: bool
    botScope: BotScope
