import telebot
from telebot.handler_backends import StatesGroup, State

from funcs.database_funcs import add_note_to_db, add_user_to_db, get_notes_from_category, delete_notes_db
from funcs.datetime_funcs import get_welcome
from funcs.help_funcs import get_rus_category, isCorrectInput
from init_bot import bot
from keyboards.inline import categories_keyboard, exit_the_category_keyboard, delete_notes_keyboard, consent_keyboard
from keyboards.reply import get_basic_keyboard


class States(StatesGroup):
    wait_category_for_add = State()
    wait_note = State()
    wait_category_for_select = State()
    wait_numbers_for_delete = State()


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    markup = get_basic_keyboard()
    add_user_to_db(telegram_id=message.from_user.id, name=message.from_user.username)
    bot.send_message(
        message.chat.id,
        text=f"{get_welcome(name=message.from_user.username)} Я бот для заметок.",
        reply_markup=markup
    )
