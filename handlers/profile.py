from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from filters.is_student import IsStudent
from filters.is_teacher import IsTeacher
from keyboards.global_menu import global_menu_student
from utils.users import Teacher, Student
from handlers.global_menu import GlobalMenu

router_profile = Router()


@router_profile.message(GlobalMenu.student, F.text == "Профиль")
async def profile1(message: Message):
    statistics = Student()
    statistics.get_statistics(message.from_user.id)
    if statistics.number_of_task != 0:
        await message.answer(f"""
ФИ: {statistics.name}
Класс обучения: {statistics.class_number}
Id: {message.from_user.id} - скажи его своему преподавателю
Процент правильных: {round(statistics.correct_answer / statistics.number_of_task * 100)}%
Правильных: {statistics.correct_answer}
Ошибок: {statistics.number_of_task - statistics.correct_answer}
    """, reply_markup=global_menu_student.markup)
    else:
        await message.answer(f"""
ФИ: {statistics.name}
Класс обучения: {statistics.class_number}
Id: {message.from_user.id} - скажи его своему преподавателю
Процент правильных: Вы не решали задания
Правильных: Вы не решали задания
Ошибок: Вы не решали задания
    """, reply_markup=global_menu_student.markup)

@router_profile.message(GlobalMenu.teacher and F.text == "Профиль")
async def profile2(message: Message):
    statistics = Teacher()
    statistics.get_statistics(message.from_user.id)
    photo = FSInputFile('IMG_20241115_111513.jpg')
    if statistics.number_of_students != 0:
        await message.answer_photo(photo=photo, caption=f"""
ФИ: {statistics.name}
Количество учеников: {statistics.number_of_students}
Общий процент правильности: {round(statistics.correct_answer/statistics.number_of_task*100)}%


Посмотреть статистику по ученикам:
""")
    else:
        await message.answer_photo(photo=photo, caption=f"""
ФИ: {statistics.name}
Количество учеников: {statistics.number_of_students}
Общий процент правильности: Вы не выдавали заданий


Посмотреть статистику по ученикам:
""")
