from aiogram import Bot, Dispatcher, executor, types
import markup as nav
from db import BotDB
import re


# bot_link = 'https://t.me/tennis_spb_test_bot'
TOKEN = '5544871151:AAGz6v58fCCpGVMBRubRrBE7rxAV0xjxaCY'
db = BotDB('tennisdb.db')


# Регулярное выжарение для проверки номера телефона!
regular_number = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
# Функция для проверки сообщений на предмет посторонних символов(кроме a-z, а-я)
check = lambda s: not all('a'<=x<='z' or 'а'<=x<='я' for x in s.lower())


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

import os



print(os.getcwd( ) )



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

