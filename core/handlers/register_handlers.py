from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from core.database.create_table import User
from core.database.user_queris import create_user
from core.utils.statesform import StepForm


reg_router = Router()

# Регистрация уникального пользователя по чат id телеги
@reg_router.message(Command('register'))
async def get_register(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name},'
                         f' начинаем регистрацию. Введите имя')
    await state.set_state(StepForm.GET_NAME)


@reg_router.message(StepForm.GET_NAME)
async def get_name(message: Message, state: FSMContext):
    await message.answer('Введите отчество')
    await state.update_data(name=message.text)
    await state.set_state(StepForm.GET_MID_NAME)


@reg_router.message(StepForm.GET_MID_NAME)
async def get_name(message: Message, state: FSMContext):
    await message.answer('Введите фамилию')
    await state.update_data(mid_name=message.text)
    await state.set_state(StepForm.GET_LAST_NAME)


@reg_router.message(StepForm.GET_LAST_NAME)
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)

    context_data = await state.get_data()

    name = context_data.get('name')
    mid_name = context_data.get('mid_name')
    last_name = context_data.get('last_name')
    full_name_tg = message.from_user.full_name

    # Записать пользователя в базу данных
    new_user = create_user(name, mid_name, last_name, message.from_user.id,
             full_name_telegram=full_name_tg)

    if type(new_user) is User:
        await message.answer(f'Вы успешно зарегистрировались, как '
                             f'{new_user.first_name}'
                             f' {new_user.middle_name}'
                             f' {new_user.last_name}')
    else:
        await message.answer('Такой пользователь уже зарегистрирован')

    await state.clear()











