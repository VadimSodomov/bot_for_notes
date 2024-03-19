from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from funcs.help_funcs import get_rus_category


def categories_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton(text="Личное", callback_data="personal"),
        InlineKeyboardButton(text="Работа", callback_data="work"),
        InlineKeyboardButton(text="Учеба", callback_data="study"),
        InlineKeyboardButton(text="Планы на день", callback_data="day_plans"),
        InlineKeyboardButton(text="Другое", callback_data="other"),
        InlineKeyboardButton(text="Показать все", callback_data="all"),
    )
    return markup


def exit_the_category_keyboard(category):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"Выйти из \"{get_rus_category(category)}\"", callback_data="exit_category"))
    return markup


def delete_notes_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Удалить все", callback_data="delete_all_from_category"),
        InlineKeyboardButton(text="Удалить некоторые", callback_data="delete_certain_from_category")
    )
    return markup


def consent_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Уверен(а)", callback_data="consent_to_delete_all"),
        InlineKeyboardButton(text="Нет, это ошибка", callback_data="mistake")
    )
    return markup


def delete_all_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Удалить все", callback_data="delete_all_notes"),
    )
    return markup


def consent_delete_all_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Уверен(а)", callback_data="consent_delete_ALL"),
        InlineKeyboardButton(text="Нет, это ошибка", callback_data="mistake_ERROR")
    )
    return markup
