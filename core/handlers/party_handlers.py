from datetime import datetime, timedelta

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types

from core.database.create_table import Party
from core.database.party_queris import create_party
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

   # на урок записываем группу - то есть в таблицу лесонс хистори добавляем
   #  строку с id  групы, и записываем всех студентов из этой группы на урок
   #  (id студетов)





    await callback.message.answer(text='Группа записана')
    await callback.answer()



