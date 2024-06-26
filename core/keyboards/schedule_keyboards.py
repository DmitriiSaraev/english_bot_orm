from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.create_table import Schedule, LessonsHistory
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


# Выбор кого записать (группу или студента)
def get_keyboard_add_student_to_lesson(lesson_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='Записать группу',
                   callback_data=MainCallbackData(
                       action='show_party_for_add_lesson',
                       lesson_id=lesson_id))
    builder.button(text='Записать ученика',
                   callback_data=MainCallbackData(
                       action='add_student_to_lesson',
                       lesson_id=lesson_id))

    return builder.as_markup()


# Для записи группы на урок (выводит список групп)
def keyboard_add_party_to_lesson(lesson_id, partys):
    builder = InlineKeyboardBuilder()

    for party in partys:
        builder.button(text=f'{party.name}',
                       callback_data=
                       MainCallbackData(action='add_party_to_lesson',
                                        lesson_id=lesson_id,
                                        party_id=party.id,
                                        party_name=party.name))

    builder.adjust(*[1 for item in partys])
    return builder.as_markup()


def get_keyboard_recorded_student_to_lesson_and_edit_lesson(lessons_history):
    # получить список учеников записанных на урок и кнопки для редактирования
    builder = InlineKeyboardBuilder()

    for lesson in lessons_history:
        lesson: LessonsHistory
        lesson_id = lesson.lesson_id
        if lesson.party:
            builder.button(text=f'{lesson.party.name}',
                           callback_data=MainCallbackData(
                               action='open_party_card',
                               lesson_id=lesson.lesson_id,
                               party_id=lesson.party_id))
        else:
            builder.button(text=f'{lesson.student.first_name} {lesson.student.last_name}',
                           callback_data=MainCallbackData(
                               action='open_student_card',
                               lesson_id=lesson.lesson_id,
                               student_id=lesson.student_id)
                           ),

    builder.button(text='Записать группу',
                   callback_data=MainCallbackData(action='str', lesson_id=lesson_id))
    builder.button(text='Записать ученика',
                   callback_data=MainCallbackData(
                       action='show_student_for_add_to_lesson',
                       lesson_id=1))
    builder.button(text='Удалить ученика',
                   callback_data=MainCallbackData(
                       action='show_student_for_delete_from_lesson',
                       lesson_id=1))

    builder.adjust(1, 1, *[1 for item in lessons_history])

    return builder.as_markup()







