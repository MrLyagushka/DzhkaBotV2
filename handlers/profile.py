from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from filters.is_student import IsStudent
from filters.is_teacher import IsTeacher
from keyboards.global_menu import global_menu_student
from utils.get_statistics_student import GetStatisticsStudent
from utils.get_statistics_teacher import GetStatisticsTeacher

router_profile = Router()


@router_profile.message(F.text == "Профиль", IsStudent())
async def profile1(message: Message):
    statistics = GetStatisticsStudent(message.from_user.id)
    if statistics.number_of_task != 0:
        await message.answer(f"""
Никнейм: тута он будет\n
Процент правильных: {round(statistics.correct_answer / statistics.number_of_task * 100)}%
Правильных: {statistics.correct_answer}
Ошибок: {statistics.number_of_task - statistics.correct_answer}
    """, reply_markup=global_menu_student.markup)
    else:
        await message.answer(f"""
Никнейм: тута он будет\n
Процент правильных: Вы не решали задания
Правильных: Вы не решали задания
Ошибок: Вы не решали задания
    """, reply_markup=global_menu_student.markup)

@router_profile.message(F.text == "Профиль", IsTeacher())
async def profile2(message: Message):
    statistics = GetStatisticsTeacher(message.from_user.id)
    photo = FSInputFile('C:/Users/Олег/Pictures/tralyalya.png')
    if statistics.number_of_students != 0:
        await message.answer_photo(photo=photo, caption=f"""
Никнейм: тута он будет
Количество учеников: {statistics.number_of_students}
Общий процент правильности: {round(statistics.correct_answer/statistics.number_of_task*100)}%


Посмотреть статистику по ученикам:
""")
    else:
        await message.answer_photo(photo=photo, caption=f"""
Никнейм: тута он будет
Количество учеников: {statistics.number_of_students}
Общий процент правильности: Вы не выдавали заданий


Посмотреть статистику по ученикам:
""")