import telebot

from config import TOKEN

bot = telebot.TeleBot(TOKEN, state_storage=telebot.StateMemoryStorage())