from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

import markup as nav
from config import dp
from timechoose import clock_callback as clock_cal_callback, TimeChoose


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
