import telebot

from funcs.database_funcs import add_note_to_db
from funcs.help_funcs import get_rus_category
from handlers.user import States
from init_bot import bot
from keyboards.inline import categories_keyboard, exit_the_category_keyboard


@bot.message_handler(func=lambda message: message.text == "Добавить заметку")
def command_add_note(message: telebot.types.Message):
    markup = categories_keyboard()
    bot.send_message(
        message.chat.id,
        text="Выбери категорию для добавления заметки:",
        reply_markup=markup
    )
    bot.set_state(message.from_user.id, States.wait_category_for_add, message.chat.id)


@bot.callback_query_handler(func=lambda callback: True, state=States.wait_category_for_add)
def button_add_note(callback: telebot.types.CallbackQuery):
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data["category_to_add"] = callback.data
        category = callback.data
    bot.edit_message_text(
        text=f"[{get_rus_category(category)}] Введите, пожалуйста, заметку:",
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        reply_markup=None
    )
    bot.set_state(callback.from_user.id, States.wait_note, callback.message.chat.id)


@bot.message_handler(state=States.wait_note)
def add_note(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        category = data["category_to_add"]
        add_note_to_db(note=message.text, telegram_id=message.from_user.id, category=category)
    markup = exit_the_category_keyboard(category)
    bot.send_message(
        message.chat.id,
        text=f"Заметка добавлена! Можете продолжать писать заметки для этой категории",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda callback: callback.data == "exit_category")
def exit_category(callback: telebot.types.CallbackQuery):
    bot.edit_message_text(
        text="Заметка добавлена! Выберите дальнейшее действие в меню",
        reply_markup=None, chat_id=callback.message.chat.id, message_id=callback.message.id)
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
