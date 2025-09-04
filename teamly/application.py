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

from .types.application import Application as ApplicationPayload
from typing import TYPE_CHECKING, Any, Dict, List, Literal

if TYPE_CHECKING:
    from .state import ConnectionState

class Application:

    def __init__(
        self,
        state: ConnectionState,
        data: ApplicationPayload,
        teamId: str
    ) -> None:
        self._state: ConnectionState = state
        self.id: str = data['id']
        self.type: str = data['type']
        self.submitted_by: Dict[str, Any] = data['submittedBy']
        self.answers: List[Dict[str, Any]] = data['answers']
        self.status: Literal['pending', 'approved', 'rejected'] = data['status']
        self.created_at: str = data['createdAt']
        self.team_id: str = teamId

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "submittedBy": self.submitted_by,
            "answers": self.answers,
            "status": self.status,
            "createdAt": self.created_at
        }

    async def update_status(self, status: Literal['accepted', 'rejected']):
        await self._state.http.update_application_status(teamId=self.team_id, applicationId=self.id, status=status)
        pass

    def __repr__(self) -> str:
        return f"<Application id={self.id} submittedBy={self.submitted_by['id']} status={self.status!r}>"
