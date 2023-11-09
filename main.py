from aiogram import Bot
import asyncio
import logging

from core.handlers.basic import dp
from core.handlers.create_new_lesson import create_lesson_router
from core.handlers.party_handlers import party_router
from core.handlers.register_handlers import reg_router
from core.handlers.schedule_handlers import schedule_router
from core.handlers.student_handlers import student_router
from core.settings import settings


async def start(dp):
    dp.include_router(reg_router)
    dp.include_router(schedule_router)
    dp.include_router(student_router)
    dp.include_router(create_lesson_router)
    dp.include_router(party_router)

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token='6819178630:AAFdfIgpzZVotZqLfSQnNHqLWZBbv3l-3lg', parse_mode='HTML')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start(dp))
