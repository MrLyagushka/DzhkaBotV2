from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.users import Student


class IsStudent(BaseFilter):

    def __init__(self) -> None:
        self.student = list(map(lambda x: x[0], Student().student))

    async def __call__(self, message: Message) -> bool:
        self.student = list(map(lambda x: x[0], Student().student))
        return message.from_user.id in self.student
