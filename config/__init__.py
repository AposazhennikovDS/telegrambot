import logging
import re
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db import BotDB

# Базовые настройки.
logging.basicConfig(level=logging.INFO)
TOKEN = '5544871151:AAGz6v58fCCpGVMBRubRrBE7rxAV0xjxaCY'
bot = Bot(token=TOKEN)
db = BotDB("tennisdb.db")
dp = Dispatcher(bot, storage=MemoryStorage())


# Регулярное выражение для проверки номера телефона! Используется при регистрации и в функции изменения номера телефона.
# regular_number = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
regular_number = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
# Функция для проверки фамилии и имени! Используется при регистрации и в функции изменения номера телефона.
check = lambda s: not all('a'<=x<='z' or 'а'<=x<='я' for x in s.lower())