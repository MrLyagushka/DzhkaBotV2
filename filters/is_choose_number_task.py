from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.get_student import GetStudent


class IsChooseNumberTask(BaseFilter):
    #
    # def __init__(self):

    async def __call__(self, message: Message) -> bool:
        for number in range(1,26+1):
            if message.text == f"№{number}":
                return True
        return False
