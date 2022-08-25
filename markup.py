from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ------------------- Main Menu-------------------





"""Создаем кнопки в главном меню"""

btnRent = KeyboardButton('Записаться на корт')
btnMyRents = KeyboardButton('Мои записи')
btnTimeTable = KeyboardButton('Посмотреть расписание')
btnProfile = KeyboardButton('Посмотреть анкету')
btnMain = KeyboardButton('Главное меню')







MainMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnProfile,
                                                btnTimeTable,
                                                btnRent,
                                                btnMyRents)





# ------------------- Rent Court Menu -------------------


"""Логика такая: человек нажимает 'Выбрать дату',  ему предлагается
посмотреть расписание, если он согласился перекидываем его в {btnTimeTable},
 если отказался -> 'Выбрать корт'(1/2), -> 'Выбрать тип тренировки' 
 -> просим написать время в минутах, 
 спрашиваем подтвердить запись или начать сначала запись'"""

btnChooseDate = KeyboardButton('Выбрать дату')
btnChooseCourt = KeyboardButton('Выбрать корт')
btnChooseType = KeyboardButton('Выбрать тип записи')
btnCourt1 = KeyboardButton('Корт №1(Правый)')
btnCourt2 = KeyboardButton('Корт №2(Левый)')
btnType1 = KeyboardButton('Открытая тренировка')
btnType2 = KeyboardButton('Закрытая тренировка')
btnAccept = KeyboardButton('Подтвердить запись?(Да/Нет)')
btnBackToRent = KeyboardButton('Начать запись сначала')


# Основная функция для формирования меню "Записаться на корт"
RentMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnChooseDate, btnMain)



# Функция для формирования меню выбора корта (1/2)
ChooseCourtMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnCourt1, btnCourt2, btnBackToRent)



# Функция для формирования меню  при нажатии на 'Выбрать тип записи' (Открытая/Закрытая)
ChooseTypeMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnType1, btnType2, btnBackToRent)


# ------------------- My Rents Menu -------------------
"""При нажатии этой кнопки в главном меню человек может выбрать какие 
записи он хочет посмотреть, в меню 'Предстоящие записи' он, также,
 может изменить или удалить запись """

btnFutureRents = KeyboardButton('Предстоящие записи')
btnPreviousRents = KeyboardButton('Предыдущие записи')
btnEditRent = KeyboardButton('Редактировать запись')
btnDeleteRent = KeyboardButton('Удалить запись')
btnBactToMyRents = KeyboardButton('Мои записи')


# Основная функция для формирования меню "Мои записи"
MyRentsMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnFutureRents,btnPreviousRents , btnMain)


# Функция для формирования меню при нажатии на "Предстоящие записи"
FutureRentsMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnEditRent,btnDeleteRent, btnBactToMyRents)



# ------------------- Timetable Menu -------------------

"""Логика такая: человек выбирает дату и ему показывает все расписание на весь день, " \
"из этого меню можно сразу уйти в 'Записаться на корт' """


# Основная функция для формирования меню "Посмотреть расписание"
TimeTableMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnChooseDate, btnRent, btnMain)


# ------------------- Profile Menu -------------------
"""В будущем здесь будеть кнопка найти оппонента, 
когда мы реализуем функцию рейтинга через ИИ"""


btnEditRent = KeyboardButton('Редактировать профиль')

btnNewRegistration = KeyboardButton('Пройти регистрацию сначала')
btnNewFirstName = KeyboardButton('Изменить имя')
btnNewLastName = KeyboardButton('Изменить фамилию')
btnNewAge = KeyboardButton('Изменить возраст')
btnNewPhoto = KeyboardButton('Изменить/Добавить фото')




# Основная функция для формирования меню "Посмотреть анкету"
ProfileMenu = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnEditRent, btnMain)
EditProfile = ReplyKeyboardMarkup(resize_keyboard = True).\
                                            add(btnNewRegistration, btnNewFirstName, btnNewLastName, btnNewAge, btnNewPhoto, btnMain)