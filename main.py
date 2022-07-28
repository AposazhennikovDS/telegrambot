from aiogram import Bot, Dispatcher, executor, types
import markup as nav
from db import BotDB


# bot_link = 'https://t.me/tennis_spb_test_bot'
TOKEN = '5544871151:AAGz6v58fCCpGVMBRubRrBE7rxAV0xjxaCY'
db = BotDB('tennisdb.db')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Функция для проверки сообщений на предмет посторонних символов(кроме a-z, а-я)
check = lambda s: not all('a'<=x<='z' or 'а'<=x<='я' for x in s.lower())


# Функция запускает процесс регистрации:
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Для того, чтобы впервые записатсья на корт"
                                                     " потребуется регистрация, пожалуйста напиши свое имя(без фамилии): ")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup= nav.MainMenu)







# Обработчик сообщений
@dp.message_handler()
async def bot_message(message: types.Message):

    if message.chat.type == 'private':

        if message.text == "Записаться на корт":
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                                 format(message.from_user), reply_markup=nav.RentMenu)
        elif message.text == "Мои записи":
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                                 format(message.from_user), reply_markup=nav.MyRentsMenu)
        elif message.text == "Посмотреть расписание":
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.
                                 format(message.from_user), reply_markup=nav.TimeTableMenu)
        elif message.text == "Посмотреть анкету":
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.send_message(message.from_user.id,'Привет {0.first_name}'.
                                 format(message.from_user), reply_markup=nav.ProfileMenu)
        elif message.text == "Главное меню":
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.send_message(message.from_user.id,'Привет {0.first_name}'.
                                 format(message.from_user), reply_markup=nav.MainMenu)
        elif message.text == "Выбрать дату":
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.send_message(message.from_user.id,'Привет {0.first_name}'.
                                 format(message.from_user), reply_markup=nav.MainMenu)

        elif db.get_signup(message.from_user.id) == 'setfirstname':
            if(len(message.text) > 15):
                await bot.send_message(message.from_user.id, "Слишком длинное имя, укажите имя без фамилии")
            elif not check(message.text):
                await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ, "
                                                             "имя должно состоять только из букв русского или "
                                                             "латинского алфавита")
            else:
                db.set_first_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "setlastname")
                await bot.send_message(message.from_user.id, "Отлично! Двигаемся дальше! Напиши свою Фамилию(без имени): ")

        elif db.get_signup(message.from_user.id) == "setlastname":
            if(len(message.text) > 20):
                await bot.send_message(message.from_user.id, "Слишком длинная фамилия, укажите настоящую фамилию: ")
            elif (len(message.text) < 4):
                await bot.send_message(message.from_user.id, "Слишком короткая фамилия, укажите настоящую фамилию: ")
            elif not check(message.text):
                await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ, "
                                                             "фамилия должна состоять только из букв русского или латинского алфавита. Попробуйте снова: ")
            else:
                db.set_last_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "setphonenumber")
                await bot.send_message(message.from_user.id,
                                       "Ты просто супер! Мы почти у цели! Оставь свой номер телефона в формате (8XXXXXXXXXX), "
                                       "чтобы мы могли с тобой связаться, если не хочешь оставлять номер, просто напиши 0 в ответном сообщении️: ")

        elif db.get_signup(message.from_user.id) == "setphonenumber":
            if (len(message.text) > 11):
                await bot.send_message(message.from_user.id, "Ошибка! Слишком много цифр, если не хотите оставлять номер, отправьте 0 в ответном сообщении")
            elif not (message.text.isdigit()):
                await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ, "
                                                             "фамилия должна состоять только из букв русского или латинского алфавита. Попробуйте снова: ")
            else:
                db.set_phone_number(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "done")
                await bot.send_message(message.from_user.id, "Вы успешно зарегистрированы!", reply_markup=nav.MainMenu)




# @dp.message_handler(commands='test')
# async def test(message: types.message):
#        global button
#        global reply
#     #    создаем глобальные переменные
#        reply = message.chat.id
#        keyboard_markup = types.InlineKeyboardMarkup()
#        btn = types.InlineKeyboardButton('Button', callback_data= 'press')
#        keyboard_markup.row(btn)
#        button = await bot.send_message(message.chat.id, 'Test', reply_markup=keyboard_markup)
# @dp.callback_query_handler(lambda c: c.data == 'press')
# async def delete_test(call: types.CallbackQuery ):
#     # types.CallbackQuery просто затычка, если нужна другая доп. функция, можно поставить вместо затычки
#     await bot.send_message(reply, 'Second test')
#     await button.delete()















if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

