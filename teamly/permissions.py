
from __future__ import annotations
from typing import Optional, Self

from teamly.flags import BaseFlags


class Permissions:

    VALUES = (
        'administrator',
        'manage_channels',
        'manage_roles',
        'manage_team',
        'view_audit_log',
        'ban_members',
        'delete_messages',
        'manage_applications',
        'join_tournaments',
        'create_invites',
        'mention_everyone_and_here',
        'manage_blogs',
        'kick_members',
        'move_members'
    )

    def __init__(self, value: int = 0, **kwargs: Optional[bool]) -> None:
        self.value: int = value

        for k,v in kwargs.items():
            if k not in self.VALUES:
                raise ValueError(f"Unknown permission: '{k}'")
            if v is True:
                i = self.VALUES.index(k)
                self.value |= (1 << i)

    @classmethod
    def none(cls) -> int:
        return 0

    @classmethod
    def all(cls) -> Self:
        return cls(0b0000_0011_1111_1111_1111)

    @property
    def administrator(self) -> int:
        return 1 << 0

    @property
    def manage_channels(self) -> int:
        return 1 << 1

    @property
    def manage_roles(self) -> int:
        return 1 << 2

    @property
    def manage_team(self) -> int:
        return 1 << 3

    @property
    def view_audit_log(self) -> int:
        return 1 << 4

    @property
    def ban_members(self) -> int:
        return 1 << 5

    @property
    def delete_messages(self) -> int:
        return 1 << 6

    @property
    def manage_applications(self) -> int:
        return 1 << 7

    @property
    def join_tournaments(self) -> int:
        return 1 << 8

    @property
    def create_invites(self) -> int:
        return 1 << 9

    @property
    def mention_everyone_and_here(self):
        return 1 << 10

    @property
    def manage_blogs(self):
        return 1 << 11

    @property
    def kick_members(self):
        return 1 << 12

    @property
    def move_members(self):
        return 1 << 13

    def has(self, name: str) -> bool:
        try:
            index = self.VALUES.index(name)
        except ValueError:
            raise ValueError(f"Unknown permission: {name}")
        return bool(self.value & (1 << index))

    def enable(self, name: str) -> None:
        index = self.VALUES.index(name)
        self.value |= (1 << index)

    def disable(self, name: str) -> None:
        index = self.VALUES.index(name)
        self.value &= ~(1 << index)

    def __repr__(self) -> str:
        enabled = [name for i, name in enumerate(self.VALUES) if self.value & (1 << i)]
        return f"<Permissions value={self.value} enabled={enabled}>"



class PermissionsOverwrite(BaseFlags):

    def __init__(self) -> None:
        raise RuntimeError(
            "Use PermissionsOverwrite.text(), .voice(), etc. — do not instantiate directly."
        )

    @classmethod
    def text(cls, **kwargs: Optional[bool]) -> Self:
        self = cls.__new__(cls)
        self._type = "text"
        self.allow = Permissions.none()
        self.deny = Permissions.none()
        for i, name in enumerate(cls.TEXT):
            if kwargs.keys() not in cls.TEXT:
                raise ValueError(f"'{name}' is not a valid permission for this channel type")
            if name in kwargs.keys():
                bit = kwargs.get(name)
                if bit is True:
                    self.allow |= (1 << i)
                if bit is False:
                    self.deny |= ~(1 << i)

        return self

    @classmethod
    def voice(cls, **kwargs: Optional[bool]) -> Self:
        self = cls.__new__(cls)
        self._type = "voice"
        self.allow = Permissions.none()
        self.deny = Permissions.none()
        for i, name in enumerate(cls.VOICE):
            if kwargs.keys() not in cls.VOICE:
                raise ValueError(f"'{name}' is not a valid permission for this channel type")
            if name in kwargs.keys():
                bit = kwargs.get(name)
                if i != 7:
                    if bit is True:
                        self.allow |= (1 << i)
                    if bit is False:
                        self.deny |= ~(1 << i)
                else:
                    if bit is True:
                        self.allow |= (1 << 12)
                    if bit is False:
                        self.deny |= ~(1 << 12)

        return self

    @classmethod
    def todo(cls, **kwargs: Optional[bool]) -> Self:
        self = cls.__new__(cls)
        self._type = "todo"
        self.allow = Permissions.none()
        self.deny = Permissions.none()
        for i, name in enumerate(cls.TODO):
            if kwargs.keys() not in cls.TODO:
                raise ValueError(f"'{name}' is not a valid permission for this channel type")
            if name in kwargs.keys():
                bit = kwargs.get(name)
                if bit is True:
                    self.allow |= (1 << i)
                if bit is False:
                    self.deny |= (1 << i)

        return self

    @classmethod
    def watchstream(cls, **kwargs: Optional[bool]) -> Self:
        self = cls.__new__(cls)
        self._type = "watchstream"
        self.allow = Permissions.none()
        self.deny = Permissions.none()
        for i, name in enumerate(cls.WATCHSTREAM):
            if kwargs.keys() not in cls.WATCHSTREAM:
                raise ValueError(f"'{name}' is not a valid permission for this channel type")
            if name in kwargs.keys():
                bit = kwargs.get(name)
                if bit is True:
                    self.allow |= (1 << i)
                if bit is False:
                    self.deny |= (1 << i)

        return self

    @classmethod
    def announcement(cls, **kwargs: Optional[bool]):
        self = cls.__new__(cls)
        self._type = "announcement"
        self.allow = Permissions.none()
        self.deny = Permissions.none()
        for i, name in enumerate(cls.ANNOUNCEMENT):
            if kwargs.keys() not in cls.ANNOUNCEMENT:
                raise ValueError(f"'{name}' is not a valid permission for this channel type")
            if name in kwargs.keys():
                bit = kwargs.get(name)
                if bit is True:
                    self.allow |= (1 << i)
                if bit is False:
                    self.deny |= (1 << i)

        return self


    def has(self, name: str) -> Optional[bool]:
        """Return the state of a permission in this overwrite.

        Parameters
        ----------
        name: str
            The permission name to check.

        Returns
        -------
        Optional[bool]
            ``True`` if the permission is explicitly allowed, ``False`` if it is
            explicitly denied and ``None`` if it is not specified in this
            overwrite.
        """

        type_map = {
            "text": self.TEXT,
            "voice": self.VOICE,
            "todo": self.TODO,
            "watchstream": self.WATCHSTREAM,
            "announcement": self.ANNOUNCEMENT,
        }

        if not hasattr(self, "_type"):
            raise RuntimeError("PermissionsOverwrite not initialised correctly")

        valid = type_map.get(self.__type)
        if valid is None or name not in valid:
            raise ValueError(f"'{name}' is not a valid permission for this channel type")

        index = valid.index(name)
        if self.__type == "voice" and index == 7:
            index = 12

        allowed = bool(self.allow & (1 << index))
        denied = bool(self.deny & (1 << index))

        if allowed:
            return True
        if denied:
            return False
        return None

    def to_dict(self):
        return {"allow": self.allow,"deny": self.deny}
