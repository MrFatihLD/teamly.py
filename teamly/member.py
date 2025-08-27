'''
MIT License

Copyright (c) 2025 Fatih Kuloglu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from __future__ import annotations

from datetime import datetime, timezone

from .user import _UserTag
from .types.member import Member as MemberPayload
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .state import ConnectionState


class Member(_UserTag):

    def __init__(self, state: ConnectionState, data: MemberPayload) -> None:
        self._state: ConnectionError = state

        self.id: str = data['id']
        self.username: str = data['username']
        self.permissions: str = data['permissions']
        self.roles: List[str] = data['roles']
        self.joined_at: str = data['joinedAt']

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _UserTag) and self.id == other.id

    def __repr__(self) -> str:
        return f"<Member id={self.id} username={self.username} joinedAt={self.joined_at}>"
