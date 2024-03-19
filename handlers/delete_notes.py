import telebot

from funcs.database_funcs import delete_notes_db, delete_all_notes_from_user_db
from funcs.help_funcs import get_rus_category, isCorrectInput
from handlers.user import States
from init_bot import bot
from keyboards.inline import consent_keyboard, consent_delete_all_keyboard


@bot.callback_query_handler(func=lambda callback: callback.data == "delete_all_from_category")
def button_delete_all_from_category(callback: telebot.types.CallbackQuery):
    markup = consent_keyboard()
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        category = data["current_category_select"]
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f"Уверены, что хотите удалить все заметки из \"{get_rus_category(category)}\"?",
        reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == "consent_to_delete_all" or callback.data == "mistake")
def delete_all_from_category(callback: telebot.types.CallbackQuery):
    if callback.data == "consent_to_delete_all":
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            category = data["current_category_select"]
        delete_notes_db(category=category, telegram_id=callback.from_user.id)
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f"Все заметки из категории \"{get_rus_category(category)}\" успешно удалены!",
            reply_markup=None)
    else:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f"Данные не удалены. Пожалуйста, будьте в следующий раз внимательнее)",
            reply_markup=None)


@bot.callback_query_handler(func=lambda callback: callback.data == "delete_certain_from_category")
def button_delete_certain_from_category(callback: telebot.types.CallbackQuery):
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data["current_message_id"] = callback.message.id
    bot.send_message(
        callback.message.chat.id,
        "Введите номера заметок\nФормат: числа через запятую без пробелов\nНапример, \"1\" или \"1,2,3\""
    )
    bot.set_state(callback.from_user.id, States.wait_numbers_for_delete, callback.message.chat.id)


@bot.message_handler(state=States.wait_numbers_for_delete)
def delete_certain_from_category(message: telebot.types.Message):
    numbers = message.text.split(",")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        current_notes = data["current_notes"].split("\n")
        current_category = data["current_category_select"]
    print(numbers, current_notes)
    if not isCorrectInput(numbers, len(current_notes)):
        bot.send_message(message.chat.id, "Неверный ввод, обратите, пожалуйста, внимание на формат ввода")
    else:
        if current_notes[0] != "":
            delete_notes = [current_notes[int(c)-1] for c in numbers]
            delete_notes_db(category=current_category, notes=delete_notes, telegram_id=message.from_user.id)
            bot.send_message(message.chat.id, f"Выбранные заметки успешно удалены из категории \"{get_rus_category(current_category)}\"")
        else:
            bot.send_message(message.chat.id, "Заметок в этой категории нет, стало быть, удалять нечего)")
        bot.set_state(message.from_user.id, States.wait_category_for_select, message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data == "delete_all_notes")
def button_delete_all_notes(callback: telebot.types.CallbackQuery):
    markup = consent_delete_all_keyboard()
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=f"Уверены, что хотите удалить все заметки?",
        reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == "consent_delete_ALL" or callback.data == "mistake_ERROR")
def delete_all_notes(callback: telebot.types.CallbackQuery):
    if callback.data == "consent_delete_ALL":
        delete_all_notes_from_user_db(telegram_id=callback.from_user.id)
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f"Все заметки успешно удалены!",
            reply_markup=None)
    else:
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f"Данные не удалены. Пожалуйста, будьте в следующий раз внимательнее)",
            reply_markup=None)
