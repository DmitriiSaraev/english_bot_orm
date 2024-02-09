from aiogram import Bot


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f'сообщение из шедулера')
