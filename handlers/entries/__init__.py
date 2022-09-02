from aiogram import types

import markup as nav
from FSM import MakeAnEnry
from config import dp, db, bot, check, regular_number, re, FSMContext
from handlers.registration.start import user_profile
from aiogram import types
from FSM import Registration
from config import dp, re, FSMContext


# @dp.message_handler(state=MakeAnEnry.date)
# async def save_date(message: types.Message, state: FSMContext) -> None:
#     await bot.send_message(message.from_user.id, f"Имя было изменено на:  {message.text}", reply_markup=nav.ProfileMenu)
#
#     db.set_db_args(message.from_user.id, first_name=message.text)
#
#     await state.finish()
#     await user_profile(message)
