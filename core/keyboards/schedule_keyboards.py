from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.create_table import Schedule
from core.utils.callback_data import MainCallbackData


def get_keyboard_for_schedule():
    builder = InlineKeyboardBuilder()
    builder.button(text='Просмотреть расписание',
                   callback_data='get_schedule')
    builder.button(text='Добавить урок',
                   callback_data='add_lesson')

    # builder.adjust(1,1,1) сколько кнопок вывести в ряду
    # (по одной, в трех рядах)

    return builder.as_markup()


def get_keyboard_lessons(lessons):
    builder = InlineKeyboardBuilder()

    for lesson in lessons:
        builder.button(
            text=f"{lesson.date.day} {lesson.start_lesson} - {lesson.end_lesson}",
            callback_data=MainCallbackData(
                action='open_lesson', lesson_id=lesson.id)
                       )

    # Для вывовода по одной кномпке в ряду
    builder.adjust(*[1 for item in lessons])

    return builder.as_markup()


def get_keyboard_id_lesson(lesson: Schedule):
    builder = InlineKeyboardBuilder()

    builder.button(text='Ученики',
                   callback_data=
                   MainCallbackData(action='get_student_from_lesson',
                                    lesson_id=lesson.id))
    # builder.button(text='Изменить время',
    #                callback_data=MainCallbackData(
    #                    action='edit_date', lesson_id=int(lesson['id_lesson'])))
    # builder.button(text='Отправить соообщение ученикам',
    #                callback_data='send_message_lesson_student')
    # builder.button(text='Отменить урок',
    #                callback_data=MainCallbackData(
    #                    action='delete_lesson',
    #                    lesson_id=int(lesson['id_lesson'])
    #                ))

    builder.adjust(1, 1, 1, 1, 1, 1, 1)

    return builder.as_markup()