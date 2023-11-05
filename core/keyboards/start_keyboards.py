from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard_for_admin():
    builder = InlineKeyboardBuilder()
    builder.button(text='Расписание',
                   callback_data='get_buttons_for_work_schedule')
    builder.button(text='Ученики',
                   callback_data='get_buttons_for_work_students')
    builder.button(text='Рассылка',
                   callback_data='newsletter')

    # builder.adjust(1,1,1) сколько кнопок вывести в ряду
    # (по одной, в трех рядах)

    return builder.as_markup()