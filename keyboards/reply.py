from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_basic_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    markup.add(
        KeyboardButton("Добавить заметку"),
        KeyboardButton("Посмотреть мои заметки"),
        KeyboardButton("/help"))
    return markup
