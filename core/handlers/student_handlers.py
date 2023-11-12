from aiogram import F, Router
from aiogram import types

from core.keyboards.student_keyboards import keyboard_for_working_with_students

student_router = Router()


@student_router.callback_query(F.data == 'get_buttons_for_work_students')
async def get_buttons_for_work_students_handler(callback: types.CallbackQuery):
    keyboard = keyboard_for_working_with_students()

    await callback.message.answer(text='Выбирай',
                                  reply_markup=keyboard)

    await callback.answer()


