from handlers.menu.calendar_date_and_time import SimpleCalendar, TimeChoose
from handlers.profile_edit.changes import *
from handlers.registration.start import user_profile
from FSM import ChooseDateTime, MakeAnEnry







# Функция для запуска сценария меню, у нас повторяются действия при запуске любого сценария меню, за исключением
# небольших нюансов, эта функция уменьшает количество дублирующегося кода.

async def menu_scenario(bot, message, mark):
    # Удаляем сообщение пользователя
    await bot.delete_message(message.from_user.id, message.message_id)
    # Создаем следующий сценарий меню и пишем сообщением название пункта меню, куда перешел пользователь
    await bot.send_message(message.from_user.id, message.text, reply_markup=mark)


# Обработчик сообщений основной
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == "Мои записи": await menu_scenario(bot, message, nav.MyRentsMenu),
    elif message.text == "Посмотреть анкету":await user_profile(message),
    elif message.text == "Посмотреть расписание":  await menu_scenario(bot, message, nav.TimeTableMenu),
    elif message.text == "Главное меню":  await menu_scenario(bot, message, nav.MainMenu),
    elif message.text == "Редактировать профиль":  await menu_scenario(bot, message, nav.EditProfile),
    elif message.text == "Выбрать время":  await menu_scenario(bot, message, await TimeChoose().start_clock()),
    elif message.text == "Пройти регистрацию сначала":  await cmd_edit_profile(message),
    elif message.text == "Изменить имя":  await change_name(message),
    elif message.text == "Изменить фамилию":  await change_last_name(message),
    elif message.text == "Изменить возраст":  await change_age(message),
    elif message.text == "Изменить/Добавить номер":  await change_phone_number(message),
    elif message.text == "Изменить/Добавить фото":  await change_photo(message),
    elif message.text == "Изменить описание(NTRP)":  await change_descr(message)
    elif message.text == "Выбрать дату":
        await ChooseDateTime.date.set()
        await menu_scenario(bot, message, await SimpleCalendar().start_calendar())
    elif message.text == "Записаться на корт":
        await bot.delete_message(message.from_user.id, message.message_id)
        await MakeAnEnry.date.set()
        await bot.send_message(message.from_user.id, "Выберите день: ", reply_markup=await SimpleCalendar().start_calendar())