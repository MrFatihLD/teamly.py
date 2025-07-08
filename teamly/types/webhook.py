



from typing import TypedDict


class Webhook(TypedDict):
    id: str
    channelId: str
    teamId: str
    username: str
    profilePicture: str
    token: str
    createdBy: str
    createdAt: str
    updatedAt: str
