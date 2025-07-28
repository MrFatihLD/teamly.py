
from __future__ import annotations
from typing import Optional, Self


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

        for i, name in enumerate(self.VALUES):
            if kwargs.get(name) is True:
                self.value |= (1 << i)

    @classmethod
    def none(cls) -> Self:
        return cls(0)

    @classmethod
    def all(cls) -> Self:
        return cls(0b0000_0011_1111_1111_1111)

    @property
    def administrator(self):
        return 1 << 0

    @property
    def manage_channels(self):
        return 1 << 1

    @property
    def manage_roles(self):
        return 1 << 2

    @property
    def manage_team(self):
        return 1 << 3

    @property
    def view_audit_log(self):
        return 1 << 4

    @property
    def ban_members(self):
        return 1 << 5

    @property
    def delete_messages(self):
        return 1 << 6

    @property
    def manage_applications(self):
        return 1 << 7

    @property
    def join_tournaments(self):
        return 1 << 8

    @property
    def create_invites(self):
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



class PermissionsOverwrite:
    pass
