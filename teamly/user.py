


from typing import List, Any, Dict


class User:

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.username: str = data['username']
        self.subdomain: str = data['subdomain']
        self.profilePicture: str = data['profilePicture']
        self.banner: str = data['banner']
        self.bot: bool = data['bot']
        self.system: bool = data['system']
        self.presence: int = data['presence']
        self.badges: List = data['badges']
        self.createdAt: str = data['createdAt']
        # self.lastOnline: str = createdby['lastOnline']
        self.flags: str = data['flags']
        self.userStatus: List[Any] = data.get('userStatus', [])
        self.userRPC: List[Any] = data.get('userRPC', [])
        self.connections: List[Any] = [data.get('connections', None)]

class ClientUser:
    pass
