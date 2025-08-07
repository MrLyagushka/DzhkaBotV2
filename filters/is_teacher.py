from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.users import Teacher


# class IsTeacher(BaseFilter):
#
#     def __init__(self) -> None:
#         self.teacher = GetTeacher().teachers_id
#
#     async def __call__(self, message: Message) -> bool:
#         print('---',self.teacher)
#         print('----',message.from_user.id)
#         return message.from_user.id in self.teacher

class IsTeacher(BaseFilter):

    def __init__(self) -> None:
        self.teacher = Teacher().teachers_id

    async def __call__(self, message: Message) -> bool:
        self.teacher = Teacher().teachers_id
        return message.from_user.id in self.teacher
