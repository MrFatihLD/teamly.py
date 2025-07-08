



from typing import List, Literal, TypedDict
from .user import UserPayload


class Answers(TypedDict):
    questionId: str
    answer: List[str] | str
    question: str
    optional: bool
    options: List[str]

ApplicationStatus = Literal["pending","approved","rejected"]

class Application(TypedDict):
    id: str
    type: str
    submittedBy: UserPayload
    answers: List[Answers]
    status: ApplicationStatus
    createdAt: str
