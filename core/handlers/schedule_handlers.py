from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.schedule_queries import get_all_future_lessons, \
    get_lesson_by_id, get_studens_from_lessons_history
from core.keyboards.schedule_keyboards import get_keyboard_for_schedule, \
    get_keyboard_lessons, get_keyboard_id_lesson
from core.utils.callback_data import MainCallbackData

schedule_router = Router()


# Выбираем просмотр расписания, либо создание урока
@schedule_router.callback_query(F.data == 'get_buttons_for_work_schedule')
async def action_selection_schedule(callback: types.CallbackQuery):
    await callback.message.answer(
        text='Что будешь делать?',
        reply_markup=get_keyboard_for_schedule()
    )
    await callback.answer()


# Получаем список уроков которые будут, либо кнопку для создания
@schedule_router.callback_query(F.data == 'get_schedule')
async def get_schedule(callback: types.CallbackQuery):
    lessons = get_all_future_lessons()
    keyboard = get_keyboard_lessons(lessons)

    if len(lessons) == 0:
        await callback.message.answer(text='Уроков нет.',
                                      reply_markup=keyboard)
    else:
        await callback.message.answer(text='Вот оно - расписание твоей мечты:',
                                      reply_markup=keyboard)
    await callback.answer()


@schedule_router.callback_query(MainCallbackData.filter(
    F.action == 'open_lesson'))
async def open_lesson(callback: types.CallbackQuery,
                      callback_data: MainCallbackData):
    lesson_id = callback_data.lesson_id
    lesson = get_lesson_by_id(lesson_id)

    keyboard = get_keyboard_id_lesson(lesson)

    await callback.message.answer(text=f'{lesson.date} '
                                       f'{lesson.start_lesson} - '
                                       f'{lesson.end_lesson}',
                                  reply_markup=keyboard)

    await callback.answer()


@schedule_router.callback_query(MainCallbackData.filter(
    F.action == 'get_student_from_lesson'))
async def get_student_from_lesson(callback: types.CallbackQuery,
                                  callback_data: MainCallbackData):

    lesson_id = callback_data.lesson_id
    lessons_history = get_studens_from_lessons_history(lesson_id)
    # if len(lessons_history) == 0:
    #     await callback.message.answer(text='На данный урок ни кто не записан',
    #                                   reply_markup=keyboard)
    # else:
    #     pass
    a = 1

    # lesson_id = callback_data.lesson_id
    # lesson = get_lesson_by_id(lesson_id)
    #
    # keyboard = get_keyboard_id_lesson(lesson)
    #
    # await callback.message.answer(text=f'{lesson.date} '
    #                                    f'{lesson.start_lesson} - '
    #                                    f'{lesson.end_lesson}',
    #                               reply_markup=keyboard)

    await callback.message.answer(text=f'{lesson.id}')

    await callback.answer()









