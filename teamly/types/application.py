

from __future__ import annotations

from .user import User
from teamly.enums import AppStatus
from typing import List, Optional, TypedDict, Union


class Answers(TypedDict):
    questionId: str
    answer: Optional[Union[str,List[str]]]
    question: str
    optional: bool
    options: List[str]

class Application(TypedDict):
    id: str
    type: str
    submittedBy: User
    answers: List[Answers]
    status: AppStatus
    createdAt: str
