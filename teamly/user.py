


from typing import Any, Dict, List


class User:

    def __init__(self, createdby: Dict[str,Any]) -> None:
        self.id: str = createdby['id']
        self.username: str = createdby['username']
        self.subdomain: str = createdby['subdomain']
        self.profilePicture: str = createdby['profilePicture']
        self.banner: str = createdby['banner']
        self.bot: bool = createdby['bot']
        self.system: bool = createdby['system']
        self.presence: int = createdby['presence']
        self.badges: List = createdby['badges']
        self.createdAt: str = createdby['createdAt']
        # self.lastOnline: str = createdby['lastOnline']
        self.flags: str = createdby['flags']
        #userStatus
        #userRPC
        #connections

class ClientUser:
    pass
