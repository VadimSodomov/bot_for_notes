import telebot

from funcs.database_funcs import get_notes_from_category
from funcs.help_funcs import get_rus_category
from handlers.user import States
from init_bot import bot
from keyboards.inline import categories_keyboard, delete_notes_keyboard, delete_all_keyboard


@bot.message_handler(func=lambda message: message.text == "Посмотреть мои заметки")
def command_select_notes(message: telebot.types.Message):
    markup = categories_keyboard()
    bot.send_message(message.chat.id, text="Выберите категорию для просмотра", reply_markup=markup)
    bot.set_state(message.from_user.id, States.wait_category_for_select, message.chat.id)


@bot.callback_query_handler(func=lambda callback: True, state=States.wait_category_for_select)
def button_select_notes_from_category(callback: telebot.types.CallbackQuery):
    if callback.data == "all":
        markup = delete_all_keyboard()
        notes_categories = get_notes_from_category(callback.data, callback.from_user.id)
        all_notes = {"personal": [], "work": [], "study": [], "day_plans": [], "other": []}
        categories = ["personal", "work", "study", "day_plans", "other"]
        for note_category in notes_categories:
            note = note_category[0]
            category = note_category[1]
            all_notes[category].append(note)
        print(all_notes)
        text = ""
        for i, c in enumerate(categories):
            if i == 0:
                text += f"{get_rus_category(c)}:\n- "+"\n- ".join(all_notes[c])
            else:
                text += f"\n\n{get_rus_category(c)}:\n- " + "\n- ".join(all_notes[c])
        bot.send_message(callback.message.chat.id, text=text, reply_markup=markup)

    else:
        category = callback.data
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data["current_category_select"] = category
        notes = get_notes_from_category(category=category, telegram_id=callback.from_user.id)
        text = get_rus_category(category) + ":\n"
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data["current_notes"] = ""
            for i, note in enumerate(notes):
                text += f"{i+1}) {note[0]}\n"
                data["current_notes"] += f"{note[0]}\n"
            else:
                data["current_notes"] = data["current_notes"][:-1]
        markup = delete_notes_keyboard()
        bot.send_message(callback.message.chat.id, text=text, reply_markup=markup)