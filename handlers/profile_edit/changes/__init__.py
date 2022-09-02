from aiogram import types

import markup as nav
from FSM import EditProfile, Registration
from config import dp, db, bot, check, regular_number, re, FSMContext
from handlers.registration.start import user_profile


# Этот обработчик и функция вызываются из меню "Анкета" при нажатии "Пройти регистрацию сначала".
# Или командой edit_profile, если пользователь в базе данных -> запускаем процесс, иначе сообщение про /start.
@dp.message_handler(commands=['edit_profile'])
async def cmd_edit_profile(message: types.Message) -> None:
    if db.user_exists(message.from_user.id):
        await message.answer("Процесс регистрации начался.\nНапиши свое имя(без фамилии): ")
        await Registration.first_name.set()
    else:
        await message.answer("Сперва нужно зарегистрироваться! Напиши /start для запуска процесса регистрации!")


# Функция для изменения имени, выставляем наш FSM в first_name, приглашаем написать имя.
async def change_name(message: types.Message):
    await bot.send_message(message.from_user.id, "Напиши новое имя:")
    await EditProfile.first_name.set()


# Проверочный хэндлер идентичный тому, что был при регистрации, только FSM он принимает не из класса Registration,
# а из класса EditProfile.
@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3,
                    state=EditProfile.first_name)
async def check_first_name(message: types.Message):
    await message.reply("Введи настоящее имя!")

# Хэндлер для обработки функции "Изменить имя" в цепочке меню "анкета"
# Если FSM стоит в first_name и предыдущий хэндлер пройден -> заменить в базе данных имя на текст сообщения,
# отправить сообщение об изменении, завершить FSM, отправить пользователю его профиль(ф-ция из main_menu)
@dp.message_handler(state=EditProfile.first_name)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, first_name=message.text)
    await bot.send_message(message.from_user.id, f"Имя было изменено на:  {message.text}", reply_markup=nav.ProfileMenu)
    await state.finish()
    await user_profile(message)


# Функция для изменения фамилии, выставляем наш FSM в last_name, приглашаем написать фамилию.
async def change_last_name(message: types.Message):
    await bot.send_message(message.from_user.id, "Напиши новую фамилию:")
    await EditProfile.last_name.set()


# Проверочный хэндлер идентичный тому, что был при регистрации, только FSM он принимает не из класса Registration,
# а из класса EditProfile.
@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3,
                    state=EditProfile.last_name)
async def check_last_name(message: types.Message):
    await message.reply("Введи настоящую фамилию!")


# Хэндлер для обработки функции "Изменить фамилию" в цепочке меню "анкета"
# Если FSM стоит в last_name и предыдущий хэндлер пройден -> заменить в базе данных фамилию на текст сообщения,
# отправить сообщение об изменении, завершить FSM, отправить пользователю его профиль(ф-ция из main_menu)
@dp.message_handler(state=EditProfile.last_name)
async def load_last_name(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, last_name=message.text)
    await bot.send_message(message.from_user.id, f"Фамилия была изменена на:  {message.text}",
                           reply_markup=nav.ProfileMenu)
    await state.finish()
    await user_profile(message)

# Функция для изменения фамилии, выставляем наш FSM в age, приглашаем написать фамилию.
async def change_age(message: types.Message):
    await bot.send_message(message.from_user.id, "Напиши свой возраст, сколько тебе полных лет?")
    await EditProfile.age.set()



# Проверочный хэндлер идентичный тому, что был при регистрации, только FSM он принимает не из класса Registration,
# а из класса EditProfile.
@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100 or float(message.text) < 4,
                    state=EditProfile.age)
async def check_age(message: types.Message):
    await message.reply('Введи реальный возраст!')


# Хэндлер для обработки функции "Изменить возраст" в цепочке меню "анкета"
# Если FSM стоит в age и предыдущий хэндлер пройден -> заменить в базе данных возраст на текст сообщения,
# отправить сообщение об изменении, завершить FSM, отправить пользователю его профиль(ф-ция из main_menu)
@dp.message_handler(state=EditProfile.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, age=message.text)
    await bot.send_message(message.from_user.id, f"Возраст был изменена на:  {message.text}",
                           reply_markup=nav.ProfileMenu)
    await state.finish()
    await user_profile(message)

@dp.message_handler(lambda message: not message.text.isdigit() or (
        float(message.text) != 0 and not re.match(regular_number, message.text)), state=EditProfile.phone_number)
async def check_phone_number(message: types.Message):
    await message.reply(
        'Неправильный формат номера, если не хочешь оставлять номер - просто напиши 0(ноль) в ответном сообщении: ')

async def change_phone_number(message: types.Message):
    await bot.send_message(message.from_user.id, "Напиши свой номер телефона: ")
    await EditProfile.phone_number.set()
# Хэндлер проверочный, чтобы отсечь "левые" номера, если наш FSM в режиме (phone_number) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст состоит из цифр, если цифра равна нулю или
# если прошел проверку регулярным выражением regular_number из файла config.
@dp.message_handler(state=EditProfile.phone_number)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, phone_number=message.text)
    await bot.send_message(message.from_user.id, f"Номер был изменен на:  {message.text}", reply_markup=nav.ProfileMenu)
    await state.finish()
    await user_profile(message)


async def change_photo(message: types.Message):
    await bot.send_message(message.from_user.id, "Прикрепи фото в сообщении: ")
    await EditProfile.photo.set()

@dp.message_handler(lambda message: message.text.isdigit() and float(message.text) == 0, state=EditProfile.photo)
async def check_photo_0(message: types.Message, state: FSMContext) -> None:
    await message.reply('Сохраняю профиль без фото')
    db.set_db_args(message.from_user.id, photo=message.text)
    await state.finish()
    await user_profile(message)

@dp.message_handler(lambda message: not message.text.isdigit() or not message.photo, state=EditProfile.photo)
async def check_photo(message: types.Message):
    await message.reply('Это не фотография!Если не хочешь отправлять фото напиши 0(ноль) в ответном сообщении: ')


async def change_descr(message:types.Message):
    await bot.send_message(message.from_user.id, "Напиши о себе то, что поможет другим игрокам лучше узнать тебя, например свой NTRP уровень")
    await EditProfile.description.set()

@dp.message_handler(state=EditProfile.description)
async def load_description(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, description=message.text)
    await bot.send_message(message.from_user.id, f"Описание было изменено на:  {message.text}", reply_markup=nav.ProfileMenu)
    await state.finish()
    await user_profile(message)

# Если наш FSM в режиме(photo) и прошел предыдущие два обработчика, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "photo", переключает FSM в следующий режим(description) Отправляет приглашающее сообщения для отправки описания профиля.
@dp.message_handler(content_types=['photo'], state=EditProfile.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    db.set_db_args(message.from_user.id, photo=message.photo[0].file_id)
    print(db.get_db_args(message.from_user.id, "photo"))
    await state.finish()
    await user_profile(message)