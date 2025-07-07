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

from .types.reaction import ReactedUser, ReactionPayload

from typing import List, Optional

class ReactionUser:
    def __init__(self, data: ReactedUser) -> None:
        self.user_id: Optional[str] = data.get('user_id', None)
        self.timestamb: Optional[str] = data.get('timestamp', None)

    def __repr__(self) -> str:
        return f"<ReactionUser id={self.user_id!r} at={self.timestamb}>"


class Reaction:
    def __init__(self, data: ReactionPayload) -> None:
        self.emoji_id: Optional[str] = data.get('emoji_id', None)
        self.count: Optional[str] =data.get('count', None)
        self.users: List[ReactionUser] = [ReactionUser(u) for u in data.get('users', None)]

    def __repr__(self) -> str:
        return f"<Reaction emoji={self.emoji_id!r} count={self.count} users={len(self.users)}>"
