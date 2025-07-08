
from __future__ import annotations

from .types.application import Application as ApplicationPayload, Answers as AnswersPayload, ApplicationStatus
from .user import User

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .state import ConnectionState

class ApplicationAnsweres:

    def __init__(self, data: AnswersPayload) -> None:
        self.question_id: str = data['questionId']
        self.answer: List[str] | str = data.get('answer', None)
        self.question: str = data['question']
        self.optional: bool = data['optional']
        self.options: List[str] = data['options']

    def __repr__(self) -> str:
        return f"<ApplicationAnsweres question={self.question} answere={self.answer}>"

class Application:

    def __init__(self,*, state: ConnectionState, data: ApplicationPayload) -> None:
        self.id: str = data['id']
        self.type: str =data['type']
        self.submitted_by: User = User(state=state,data=data)
        self.answeres: List[ApplicationAnsweres] = [ApplicationAnsweres(a) for a in data.get('answers',[])]
        self.status: ApplicationStatus = data['status']
        self.created_at: str = data['createdAt']

    def __repr__(self) -> str:
        return f"<Application id={self.id} submitedBy={self.submitted_by.username} status={self.status}>"
