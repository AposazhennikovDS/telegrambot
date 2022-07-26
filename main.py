import logging
from aiogram import Bot, Dispatcher, executor, types
import markup as nav


bot_link = 'https://t.me/tennis_spb_test_bot'
TOKEN = '5544871151:AAGz6v58fCCpGVMBRubRrBE7rxAV0xjxaCY'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                             format(message.from_user),
                             reply_markup=nav.MainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    # await bot.send_message(message.from_user.id, message.text)
    if message.text == "Записаться на корт":
        await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                             format(message.from_user), reply_markup=nav.RentMenu)
    elif message.text == "Мои записи":
        await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                             format(message.from_user), reply_markup=nav.MyRentsMenu)
    elif message.text == "Посмотреть расписание":
        await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                             format(message.from_user), reply_markup=nav.TimeTableMenu)
    elif message.text == "Посмотреть анкету":
        await bot.send_message(message.from_user.id,'Привет {0.first_name}'.
                             format(message.from_user), reply_markup=nav.ProfileMenu)
    elif message.text == "Главное меню":
        await bot.send_message(message.from_user.id,'Привет {0.first_name}'.
                             format(message.from_user), reply_markup=nav.MainMenu)
    elif message.text == "Выбрать дату":
        await bot.send_message(message.from_user.id,'Привет {0.first_name}'.
                             format(message.from_user), reply_markup=nav.MainMenu)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)