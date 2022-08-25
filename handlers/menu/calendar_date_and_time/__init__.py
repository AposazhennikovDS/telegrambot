from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar
import markup as nav
from timechoose import clock_callback as clock_cal_callback, TimeChoose
from aiogram import types
from FSM import ChooseDateTime
from config import dp, re, FSMContext




# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter(), state=ChooseDateTime.date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as date_time:
        selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
        if selected:
            date_time['date'] = date
            await ChooseDateTime.next()
            await callback_query.message.answer(
                f'You selected {date.strftime("%d/%m/%Y")}',
                reply_markup=await TimeChoose().start_clock()

            )


@dp.callback_query_handler(clock_cal_callback.filter(), state=ChooseDateTime.time)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as date_time:
        selected, time = await TimeChoose().process_selection(callback_query, callback_data)
        if selected:
            date_time['time'] = time
            print(date_time['date'], date_time['time'])
            await state.finish()
            await callback_query.message.answer(
                f'You selected {time}',
                reply_markup=nav.RentMenu

        )


