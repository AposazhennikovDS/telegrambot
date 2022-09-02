from aiogram.dispatcher.filters.state import StatesGroup, State



class Registration(StatesGroup):

    first_name = State()
    last_name = State()
    age = State()
    phone_number = State()
    photo = State()
    description = State()


class EditProfile(StatesGroup):

    first_name = State()
    last_name = State()
    age = State()
    phone_number = State()
    photo = State()
    description = State()
    done = State()

class ChooseDateTime(StatesGroup):


    date = State()
    time = State()

class MakeAnEnry(StatesGroup):

    date = State()
    begin_time = State()
    end_time = State()