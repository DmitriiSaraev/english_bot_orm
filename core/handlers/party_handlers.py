from datetime import datetime, timedelta

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.statesform import StateAddParty

party_router = Router()

### Блок создания группы ###
# @party_router.callback_query(F.data == 'add_party')
# async def add_new_party(callback: types.CallbackQuery,
#                             state: FSMContext):
#     await callback.message.answer(text='Введи название группы')
#     await state.set_state(StateAddParty.INPUT_NAME)
#     await callback.answer()
#
#
# @party_router.message(StateAddParty.INPUT_NAME)
# async def get_name_for_new_party(message: types.Message,
#                                  state: FSMContext):
#
#     date = datetime.now()
#     name = message.text
#
#     party = add_party(date, name)
#     await message.answer(text=f'Созданая группа: {name}')
#
#
#     await state.clear()