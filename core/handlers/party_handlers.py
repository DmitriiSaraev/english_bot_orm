from datetime import datetime, timedelta

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types

from core.database.create_table import Party
from core.database.party_queris import create_party, add_party_to_lesson, \
    get_active_party, \
    add_student_to_party_by_id
from core.database.user_queris import get_student_without_party
from core.keyboards.party_keyboards import keyboard_get_students_without_group, \
    keyboard_add_student_to_party
from core.utils.callback_data import MainCallbackData
from core.utils.statesform import StateAddParty

party_router = Router()


### Блок создания группы ###
@party_router.callback_query(MainCallbackData.filter(
    F.action == 'create_party'))
async def create_party_handler(callback: types.CallbackQuery,
                       state: FSMContext):
    await callback.message.answer(text='Введи название группы')
    await state.set_state(StateAddParty.INPUT_NAME)
    await callback.answer()


@party_router.message(StateAddParty.INPUT_NAME)
async def get_name_for_new_party(message: types.Message,
                                 state: FSMContext):
    name = message.text

    new_party = create_party(name)

    if type(new_party) is Party:
        await message.answer(text=f'Созданая группа: {new_party.name}')
    else:
        await message.answer(text=f'Группа с названием: {name}, уже есть.')

    await state.clear()

### Конец блока создания группы

# Записать группу на урок
@party_router.callback_query(MainCallbackData.filter(
    F.action == 'add_party_to_lesson'))
async def add_party_to_lesson_handler(callback: types.CallbackQuery,
                                      callback_data: MainCallbackData):

    lesson_id = callback_data.lesson_id
    party_id = callback_data.party_id
    party_name = callback_data.party_name

    lesson, created = add_party_to_lesson(party_id, lesson_id)

    if created:
        await callback.message.answer(text=f'Группа {party_name} записана')
    else:
        await callback.message.answer(text=f'Группа {party_name} уже записана')

    await callback.answer()


# Добавить ученика в группу (показать студентов и выбрать,
# потом выбрать группу)
@party_router.callback_query(MainCallbackData.filter(
    F.action == 'show_students_for_add_to_party'))
async def add_student_to_party_handler(callback: types.CallbackQuery,
                                       callback_data: MainCallbackData):
    students = get_student_without_party()

    keyboard = keyboard_get_students_without_group(
        action='show_party_for_add', students=students
    )

    await callback.message.answer(text='Выбирай ученика',
                                  reply_markup=keyboard)
    await callback.answer()


# Показать список групп для записи студента в одну из этих групп
@party_router.callback_query(MainCallbackData.filter(
    F.action == 'show_party_for_add'))
async def show_party_for_add_handler(callback: types.CallbackQuery,
                                       callback_data: MainCallbackData):
    student_id = callback_data.student_id
    partys = get_active_party()

    keyboard = keyboard_add_student_to_party(student_id, partys)
    await callback.message.answer(text='Такие вот группы у нас',
                                  reply_markup=keyboard)

    await callback.answer()


@party_router.callback_query(MainCallbackData.filter(
    F.action == 'add_student_to_party'))
async def add_student_to_party_handler(callback: types.CallbackQuery,
                                       callback_data: MainCallbackData):
    student_id = callback_data.student_id
    party_id = callback_data.party_id

    new_student_in_party, created = add_student_to_party_by_id(
        student_id, party_id
    )

    if created is True:
        await callback.message.answer(text=f'Ученик добавлен в группу')
    else:
        await callback.message.answer(text=f'Ученик уже добавлен в эту группу')

    await callback.answer()





