from aiogram import types

from FSM import Registration
from config import dp, re, FSMContext


# Ф-ция для отправки пользователю его анкеты. Получаем данные из базы и складываем их в переменную data.
# Пробуем если photo == 0 просто прислать Данные без фото, иначе отправляем с фото.
async def user_profile(message: types.Message):
    data = db.get_db_args(message.from_user.id, 'photo',
                          'first_name', 'last_name', 'age', 'phone_number', 'description')
    try:
        if int(data['photo']) == 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                        f"Номер телефона:  {data['phone_number']}\n\n{data['description']}",
                                   reply_markup=nav.ProfileMenu)
    except:
        await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'],
                             caption=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                     f"Номер телефона:  {data['phone_number']}\n\n{data['description']}",
                             reply_markup=nav.ProfileMenu)


# хэндлер = обработчик

# Команда 'старт' запускает процесс обработки хэндлером следующих сообщений, если ID пользователя не в базе данных ->
# Спрашиваем имя и переключаем FSM в первый режим - записи имени(first_name). Иначе, пишем сообщение,
# что пользователь уже зарегистрирован и выводим меню.

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    if not db.user_exists(message.from_user.id):
        await message.answer(
            "Для того, чтобы впервые записаться на корт потребуется регистрация напиши свое имя(без фамилии): ")
        await Registration.first_name.set()
    else:
        await message.answer("Вы уже зарегистрированы!", reply_markup=nav.MainMenu)


# Хэндлер проверочный, чтобы отсечь "левые" имена, если наш FSM в первом режиме(first_name) следующие сообщения
# сначала проходят через этот обработчик. Сообщение проверку проходит: Если текст не длиннее 25 символов или не
# короче 3 символов, если сообщение состоит из букв одного алфавита(англи или русск)

@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3,
                    state=Registration.first_name)
async def check_first_name(message: types.Message):
    await message.reply("Введите настоящее имя!")


# Если наш FSM в первом режиме(first_name) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "first_name", переключает FSM в следующий режим(last_name) Отправляет приглашающее сообщения для ввода фамилии.
@dp.message_handler(state=Registration.first_name)
async def load_first_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.reply('Отлично, теперь напиши свою фамилию: ')
    await Registration.next()


# Хэндлер проверочный, чтобы отсечь "левые" фамилии, если наш FSM в режиме (last_name) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст не длиннее 25 символов или не короче 3
# символов, если сообщение состоит из букв одного алфавита(англи или русск)
@dp.message_handler(lambda message: check(message.text) or len(message.text) > 25 or len(message.text) < 3,
                    state=Registration.last_name)
async def check_last_name(message: types.Message):
    await message.reply("Введи настоящую фамилию!")


# Если наш FSM в режиме(last_name) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "last_name", переключает FSM в следующий режим(age) Отправляет приглашающее сообщения для ввода возраста.
@dp.message_handler(state=Registration.last_name)
async def load_last_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.reply('Отлично, теперь напиши сколько тебе лет: ')
    await Registration.next()


# Хэндлер проверочный, чтобы отсечь "левый" возраст, если наш FSM в режиме (age) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст состоит из цифр, если цифра меньше ста, но
# больше четырех.
@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100 or float(message.text) < 4,
                    state=Registration.age)
async def check_age(message: types.Message):
    await message.reply('Введи реальный возраст!')


# Если наш FSM в режиме(age) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "age", переключает FSM в следующий режим(phone_number) Отправляет приглашающее сообщения для ввода номера телефона.
@dp.message_handler(state=Registration.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply('Так держать, теперь пришли свой номер, '
                        'если не хочешь оставлять номер - просто напиши 0(ноль) в ответном сообщении: ')
    await Registration.next()


# Хэндлер проверочный, чтобы отсечь "левые" номера, если наш FSM в режиме (phone_number) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст состоит из цифр, если цифра равна нулю или
# если прошел проверку регулярным выражением regular_number из файла config.
@dp.message_handler(lambda message: not message.text.isdigit() or (
        float(message.text) != 0 and not re.match(regular_number, message.text)),
                    state=Registration.phone_number)
async def check_phone_number(message: types.Message):
    await message.reply('Неправильный формат номера, если не хочешь оставлять номер - просто напиши 0(ноль) в '
                        'ответном сообщении: ')


# Если наш FSM в режиме(phone_number) и прошел предыдущий обработчик, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "age", переключает FSM в следующий режим(photo) Отправляет приглашающее сообщения для отправки фотографии.
@dp.message_handler(state=Registration.phone_number)
async def load_phone_number(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.reply(
        'Отлично, теперь прикрепи свою фотографию, если не хочешь напиши 0(ноль) в ответном сообщении: ')
    await Registration.next()


# Хэндлер проверочный, чтобы отсечь "левые" фото, если наш FSM в режиме (photo) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст состоит из цифр, если цифра равна нулю
# это означает, что человек не хочет оставлять фото. Тогда переключаем FSM на следующий режим (description)
# и отправляем пригласительное сообщение для описания профиля.
@dp.message_handler(lambda message: message.text.isdigit() and float(message.text) == 0, state=Registration.photo)
async def check_photo_0(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        'Расскажи немного о себе, как давно играешь в теннис? Что хочешь улучшить? Что считаешь своей сильной стороной?')
    await Registration.next()


# Хэндлер проверочный, чтобы отсечь "левые" фото, если наш FSM в режиме (photo) следующие сообщения сначала
# проходят через этот обработчик. Сообщение проверку проходит: Если текст не состоит из цифр, если
# сообщение типа "фото".
@dp.message_handler(lambda message: not message.text.isdigit() or not message.photo, state=Registration.photo)
async def check_photo(message: types.Message):
    await message.reply('Это не фотография!Если не хочешь отправлять фото напиши 0(ноль) в ответном сообщении: ')


# Если наш FSM в режиме(photo) и прошел предыдущие два обработчика, все следующие сообщения принимаются данным
# хэндлером. Функция принимаем сообщение и ничего не возвращает. Добавляет текст сообщения в словарь data с ключем
# "photo", переключает FSM в следующий режим(description) Отправляет приглашающее сообщения для отправки описания профиля.
@dp.message_handler(content_types=['photo'], state=Registration.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.reply('Расскажи немного о себе, как давно играете в теннис? Что хочешь улучшить? Что считаешь '
                        'своей сильной стороной?')
    await Registration.next()


# Довольно сложный финальный хэндлер(босс) обрабатывает сообщения если FSM в режиме description.
# Первый шаг - добавить id пользователя в таблицу, таким образом мы еще не занесли данных о пользователе,
# которые собрали ранее, но уже подготовили почву - занесли его id в базу. Занесем текст сообщения в словарь data с
# ключем description, пробуем если data["photo"] существует и не равно 0 отправить человеку фото
# со всей внесенной им информацией и тут же заносим все полученные данные из словаря data в базу данных.
# Если фотки нет, отправляем данные без фотки и загружаем данные в таблицу без фотки.
# Хвалим нашего пользователя и завершаем FSM.

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
                db.set_db_args(message.from_user.id, photo=data['photo'],
                               first_name=data['first_name'], last_name=data['last_name'], age=data['age'],
                               phone_number=data['phone_number'], description=data['description'])

        except:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Имя:  {data['first_name']},\nФамилия:  {data['last_name']},\nВозраст:  {data['age']},\n"
                                        f"Номер телефона:  {data['phone_number']}\n\n{data['description']}")
            db.set_db_args(message.from_user.id, photo=0,
                           first_name=data['first_name'], last_name=data['last_name'], age=data['age'],
                           phone_number=data['phone_number'], description=data['description'])
    await message.reply('Анкета успешно создана!')
    await state.finish()


from handlers.menu.main_menu import *
