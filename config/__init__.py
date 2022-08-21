from aiogram import Bot, Dispatcher
from db import BotDB
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
TOKEN = '5544871151:AAGz6v58fCCpGVMBRubRrBE7rxAV0xjxaCY'
bot = Bot(token=TOKEN)
db = BotDB("tennisdb.db")
dp = Dispatcher(bot, storage=MemoryStorage())


# Регулярное выжарение для проверки номера телефона!
regular_number = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
check = lambda s: not all('a'<=x<='z' or 'а'<=x<='я' for x in s.lower())


