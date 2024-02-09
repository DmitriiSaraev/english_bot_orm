from datetime import datetime, timedelta

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.database.schedule_queries import create_lesson
from core.utils.statesform import StateSchedule
from core.utils.app_scheduler_tasks import send_message_middleware

create_lesson_router = Router()


### Блок создания урока ###
@create_lesson_router.callback_query(F.data == 'add_lesson')
async def get_date_for_new_lesson(callback: types.CallbackQuery,
                                  state: FSMContext):
    await callback.message.answer(text='Введи дату урока в формате дд.мм.гг')
    await state.set_state(StateSchedule.INPUT_DATE)
    await callback.answer()


@create_lesson_router.message(StateSchedule.INPUT_DATE)
async def get_time_start_for_new_lesson(message: types.Message,
                                        state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Введи время начала урока в формате чч.мм')
    await state.set_state(StateSchedule.INPUT_START_LESSON)


@create_lesson_router.message(StateSchedule.INPUT_START_LESSON)
async def get_duration_for_new_lesson(message: types.Message,
                                      state: FSMContext):
    await state.update_data(start_time=message.text)
    await message.answer('Введи продолжительность урока в формате мм')
    await state.set_state(StateSchedule.INPUT_LESSON_DURATION)


@create_lesson_router.message(StateSchedule.INPUT_LESSON_DURATION)
async def create_new_lesson(message: types.Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    await state.update_data(duration=message.text)

    context_data = await state.get_data()

    date_string = context_data['date']
    date_format = "%d.%m.%y"
    date_object = datetime.strptime(date_string, date_format)

    start_time_string = context_data['start_time']
    start_time_format = "%H.%M"
    start_time_object = datetime.strptime(start_time_string, start_time_format)

    start_lesson = datetime(int(date_object.year), int(date_object.month),
                            int(date_object.day), int(start_time_object.hour),
                            int(start_time_object.minute))

    duration_lesson = int(context_data['duration'])
    duration_lesson = timedelta(minutes=duration_lesson)

    # Создайте объект datetime, объединяя date_object и start_time_object
    combined_datetime = datetime(date_object.year, date_object.month,
                                 date_object.day,
                                 start_time_object.hour,
                                 start_time_object.minute)

    # Добавьте интервал времени к combined_datetime
    end_lesson = combined_datetime + duration_lesson


    create_lesson(date_object, start_lesson, end_lesson)


    await message.answer(f'Создан урок дата: {date_object}\r\n'
                         f'Время начала:'
                         f' {start_lesson}\r\n'
                         f'Конец урока: {end_lesson}')

    await state.clear()

    # Тут вставить функцию создания напоминания
    apscheduler.add_job(send_message_middleware, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                        kwargs={'bot': bot, 'chat_id': message.from_user.id})

### Конец блока создания урока ###

