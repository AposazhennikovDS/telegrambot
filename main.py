from aiogram import Bot, Dispatcher, executor, types
import markup as nav
from db import BotDB
import re


# bot_link = 'https://t.me/tennis_spb_test_bot'
TOKEN = '5544871151:AAGz6v58fCCpGVMBRubRrBE7rxAV0xjxaCY'
db = BotDB('tennisdb.db')

regular_number = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'


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
        await bot.send_message(message.from_user.id, "Ты уже прошел регистрацию!", reply_markup= nav.MainMenu)



# Функция для запуска сценария меню, если пользователь отправляет сообщение с названием одной из кнопок меню
async def menu_scenario(bot, message, mark):
    # Удаляем сообщение пользователя
    await bot.delete_message(message.from_user.id, message.message_id)
    #Создаем следующий сценарий меню и пишем сообщением название пункта меню, куда перешел пользователь
    await bot.send_message(message.from_user.id, message.text, reply_markup=mark)

# Функция для упрощения условий регистрации
async def registration_state(message, bot, db, condition, text_mess, db_func):
    if condition:
        await bot.send_message(message.from_user.id, text_mess[0])
    elif condition:
        await bot.send_message(message.from_user.id, text_mess[1])
    else:
        db_func[0]()
        db_func[1]()
        await bot.send_message(message.from_user.id,text_mess[2])


# Обработчик сообщений
@dp.message_handler()
async def bot_message(message: types.Message):
        if message.text == "Записаться на корт":
            await menu_scenario(bot, message, nav.RentMenu)
        elif message.text == "Мои записи":
            await menu_scenario(bot, message, nav.MyRentsMenu)
        elif message.text == "Посмотреть расписание":
            await menu_scenario(bot, message, nav.TimeTableMenu)
        elif message.text == "Посмотреть анкету":
            await menu_scenario(bot, message, nav.ProfileMenu)
            if len(db.get_phone_number(message.from_user.id)) > 1:
                await bot.send_message(message.from_user.id, f"Имя: {db.get_first_name(message.from_user.id)}, "
                                                         f"\nФамилия: {db.get_last_name(message.from_user.id)}, "
                                                         f"\nНомер телефона: {db.get_phone_number(message.from_user.id)}")
            else:
                await bot.send_message(message.from_user.id, f"Имя: {db.get_first_name(message.from_user.id)}, "
                                                             f"\nФамилия: {db.get_last_name(message.from_user.id)}")

        elif message.text == "Главное меню":
            await menu_scenario(bot, message, nav.MainMenu)
        elif message.text == "Выбрать дату":
            await menu_scenario(bot, message, nav.MainMenu)

        elif db.get_signup(message.from_user.id) == "setfirstname":

            if (len(message.text) > 15):
                await bot.send_message(message.from_user.id, "Слишком длинное имя, укажи имя без фамилии")
            elif (len(message.text) < 3):
                await bot.send_message(message.from_user.id, "Слишком короткое имя, укажи настоящее имя: ")

            elif check(message.text):
                await bot.send_message(message.from_user.id, "Ты ввел запрещенный символ, "
                                                         "имя должно состоять только из букв русского или "
                                                         "латинского алфавита")

            else:

                db.set_first_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "setlastname")
                await bot.send_message(message.from_user.id,
                                       f"Отлично! Двигаемся дальше! Напиши свою Фамилию(без имени): ")

        elif db.get_signup(message.from_user.id) == "setlastname":

            if (len(message.text) > 20):
                await bot.send_message(message.from_user.id, "Слишком длинная фамилия, укажи настоящую фамилию: ")

            elif (len(message.text) < 4):
                await bot.send_message(message.from_user.id, "Слишком короткая фамилия, укажи настоящую фамилию: ")

            elif check(message.text):
                await bot.send_message(message.from_user.id, "Ты ввел запрещенный символ, "
                                                         "фамилия должна состоять только из букв русского или латинского алфавита. Попробуй снова: ")

            else:

                db.set_last_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "setphonenumber")
                await bot.send_message(message.from_user.id,
                                       f"Ты просто супер! Мы почти у цели! Оставь свой номер телефона, "
                                       "чтобы мы могли с тобой связаться, если не хочешь оставлять номер, просто напиши 0 в ответном сообщении️: ")

        elif db.get_signup(message.from_user.id) == "setphonenumber":

            if message.text == "0":

                db.set_phone_number(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, "done")
                await bot.send_message(message.from_user.id, f"Ты успешно завершил регистрацию!",
                                       reply_markup=nav.MainMenu)

            elif bool(re.match(regular_number, message.text)):
                    db.set_phone_number(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, f"Ты успешно завершил регистрацию!",
                                           reply_markup=nav.MainMenu)
            else:
                await bot.send_message(message.from_user.id, "Неправильный формат номера, оставь свой номер телефона, "
                                       "чтобы мы могли с тобой связаться, если не хочешь оставлять номер, просто напиши 0 в ответном сообщении: ")


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

