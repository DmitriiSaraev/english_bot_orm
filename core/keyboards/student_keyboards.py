from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.callback_data import MainCallbackData


def keyboard_for_working_with_students():
    builder = InlineKeyboardBuilder()

    builder.button(text='Добавить группу',
                   callback_data=
                   MainCallbackData(action='create_party'))
    builder.button(text='Добавить ученика в группу',
                   callback_data=
                   MainCallbackData(action='show_students_for_add_to_party'))

    builder.adjust(1, 1, 1)

    return builder.as_markup()
