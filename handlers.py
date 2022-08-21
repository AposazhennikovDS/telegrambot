from aiogram.dispatcher import FSMContext
from aiogram import types, executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from timechoose import clock_callback as clock_cal_callback, TimeChoose
import re
import markup as nav
from FSM import Registration, EditProfile
from config import db, dp, bot, regular_number, check














@dp.message_handler(commands=['edit profile'])
async def cmd_edit_profile(message: types.Message) -> None:
    if db.user_exists(message.from_user.id):
        await message.answer("Для того, чтобы впервые записаться на корт потребуется регистрация напиши свое имя(без фамилии): ")
        await Registration.first_name.set()
    else:
        await message.answer("Сперва нужно зарегистрироваться! Напишите /start для запуска процесса регистрации!")


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    if not db.user_exists(message.from_user.id):
        await message.answer("Для того, чтобы впервые записаться на корт потребуется регистрация напиши свое имя(без фамилии): ")
        await Registration.first_name.set()
    else:
        await message.answer("Вы уже зарегистрированы!", reply_markup=nav.MainMenu)

@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3, state=Registration.first_name)
async def check_first_name(message: types.Message):
    await message.reply("Введите настоящее имя!")

async def change_name(message: types.Message):
    await message.answer("Напишите новое имя:")
    await EditProfile.first_name.set()


@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3, state=EditProfile.first_name)
async def check_first_name(message: types.Message):
    await message.reply("Введите настоящее имя!")

@dp.message_handler(state=EditProfile.first_name)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, first_name=message.text)
    await bot.send_message(message.from_user.id, f"Имя было изменено на: {message.text}", reply_markup=nav.ProfileMenu)
    await EditProfile.done.set()



@dp.message_handler(state=Registration.first_name)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['first_name'] = message.text

    await message.reply('Отлично, теперь напиши свою фамилию: ')
    await Registration.next()

@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3, state=Registration.last_name)
async def check_last_name(message: types.Message):
    await message.reply("Введи настоящую фамилию!")

@dp.message_handler(state=Registration.last_name)
async def load_last_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['last_name'] = message.text

    await message.reply('Отлично, теперь напиши сколько тебе лет: ')
    await Registration.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100 or float(message.text) < 4, state=Registration.age)
async def check_age(message: types.Message):
    await message.reply('Введи реальный возраст!')

@dp.message_handler(state=Registration.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
      async with state.proxy() as data:
            data['age'] = message.text
      await message.reply('Так держать, теперь пришли свой номер, если не хочешь оставлять номер - просто напиши 0(ноль) в ответном сообщении: ')
      await Registration.next()

@dp.message_handler(lambda message:not message.text.isdigit() or (float(message.text) != 0 and not re.match(regular_number, message.text)), state=Registration.phone_number)
async def check_phone_number(message: types.Message):
    await message.reply('Неправильный формат номера, если не хочешь оставлять номер - просто напиши 0(ноль) в ответном сообщении: ')

@dp.message_handler(state=Registration.phone_number)
async def load_phone_number(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.reply('Отлично, теперь прикрепи свою фотографию, если не хочешь напиши 0(ноль) в ответном сообщении: ')
    await Registration.next()



@dp.message_handler(lambda message: message.text.isdigit() and float(message.text) == 0, state=Registration.photo)
async def check_photo_0(message: types.Message, state: FSMContext) -> None:
    await message.reply('Расскажите немного о себе, как давно играете в теннис? что хотите улучшить? что считаете своей сильной стороной?')
    await Registration.next()

@dp.message_handler(lambda message: not message.text.isdigit() or not message.photo, state=Registration.photo)
async def check_photo(message: types.Message):
    await message.reply('Это не фотография!Если не хочешь отправлять фото напиши 0(ноль) в ответном сообщении: ')

@dp.message_handler(content_types=['photo'], state=Registration.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply('Расскажите немного о себе, как давно играете в теннис? что хотите улучшить? что считаете своей сильной стороной?')
    await Registration.next()


@dp.message_handler(state=Registration.description)
async def load_desc(message: types.Message, state: FSMContext) -> None:

    db.add_user(message.from_user.id)
    async with state.proxy() as data:
        data['description'] = message.text
        try:
            if data['photo'] and data['photo'] != 0:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=data['photo'],
                                     caption=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                             f"Номер телефона:  {data['phone_number']}\n\n{data['description']}")
                db.set_db_args(message.from_user.id, photo = data['photo'],
                               first_name = data['first_name'], last_name = data['last_name'], age =data['age'],
                               phone_number = data['phone_number'], description = data['description'])

        except:
            await bot.send_message(chat_id=message.from_user.id,
                                 text=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                         f"Номер телефона:  {data['phone_number']}\n\n{data['description']}")
            db.set_db_args(message.from_user.id, photo=0,
                           first_name=data['first_name'], last_name=data['last_name'], age=data['age'],
                           phone_number=data['phone_number'], description=data['description'])


    await message.reply('Ваша акнета успешно создана!')
    print(db.get_db_args(message.from_user.id, "photo",
                   'first_name', 'last_name', 'age',
                  'phone_number', 'description'))
    await state.finish()



async def user_profile(message: types.Message):
    data = db.get_db_args(message.from_user.id, 'photo',
                          'first_name', 'last_name', 'age','phone_number', 'description')
    try:
        if int(data['photo']) == 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                        f"Номер телефона:  {data['phone_number']}\n\n{data['description']}",
                                   reply_markup=nav.ProfileMenu)
    except:
        print(data['photo'])
        await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'],
                             caption=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                     f"Номер телефона:  {data['phone_number']}\n\n{data['description']}",
                             reply_markup=nav.ProfileMenu)


# Функция для запуска сценария меню, если пользователь отправляет сообщение с названием одной из кнопок меню
async def menu_scenario(bot, message, mark):
    # Удаляем сообщение пользователя
    await bot.delete_message(message.from_user.id, message.message_id)
    #Создаем следующий сценарий меню и пишем сообщением название пункта меню, куда перешел пользователь
    await bot.send_message(message.from_user.id, message.text, reply_markup=mark)


# Обработчик сообщений
@dp.message_handler()
async def bot_message(message: types.Message):
        if message.text == "Записаться на корт":
            await menu_scenario(bot, message, nav.RentMenu)
        elif message.text == "Мои записи":
            await menu_scenario(bot, message, nav.MyRentsMenu)
        elif message.text == "Посмотреть анкету":
            await user_profile(message)
        elif message.text == "Посмотреть расписание":
            await menu_scenario(bot, message, nav.TimeTableMenu)
        elif message.text == "Главное меню":
            await menu_scenario(bot, message, nav.MainMenu)
        elif message.text == "Выбрать дату":
            await menu_scenario(bot, message, await SimpleCalendar().start_calendar())
        elif message.text == "Редактировать профиль":
            await menu_scenario(bot, message, nav.EditProfile)
        elif message.text == "Выбрать время":
            await menu_scenario(bot, message, await TimeChoose().start_clock())
        elif message.text == "Пройти регистрацию сначала":
            await cmd_edit_profile(message)
        elif message.text == "Изменить имя":
            await change_name(message)
# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=nav.MainMenu
        )


@dp.callback_query_handler(clock_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, time = await TimeChoose().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {time}',
            reply_markup=nav.RentMenu
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



