import datetime

from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar
import markup as nav
from timechoose import clock_callback as clock_cal_callback, TimeChoose
from aiogram import types
from FSM import ChooseDateTime, MakeAnEnry
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

# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter(), state=MakeAnEnry.date)
async def choose_date(callback_date_query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as date_time:
        selected, date = await SimpleCalendar().process_selection(callback_date_query, callback_data)
        if selected:
            date_time['date'] = date.date()
            await MakeAnEnry.next()
            await callback_date_query.message.answer(
                f'Вы выбрали: {date.strftime("%d/%m/%Y")}, С какого времени вы хотите записаться на корт? Выберите '
                f'ниже! ',
                reply_markup=await TimeChoose().start_clock())

@dp.callback_query_handler(clock_cal_callback.filter(), state=MakeAnEnry.begin_time)
async def choose_begin_time(callback_btime_query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as date_time:
        selected, time = await TimeChoose().process_selection(callback_btime_query, callback_data)
        if selected:
            date_time['begin_time'] = time
            print(date_time['date'], date_time['begin_time'])
            await MakeAnEnry.next()
            await callback_btime_query.message.answer(
                f'Вы выбрали запись на корт с: {time}, \nТеперь выберете до какого времени хотите записаться',
                reply_markup=await TimeChoose().start_clock())


@dp.callback_query_handler(clock_cal_callback.filter(), state=MakeAnEnry.end_time)
async def choose_begin_time(callback_etime_query: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as date_time:
        selected, time = await TimeChoose().process_selection(callback_etime_query, callback_data)
        if selected:
            date_time['end_time'] = time
            print(type(date_time['begin_time']))
            print(date_time['date'], date_time['begin_time'], date_time['end_time'])
            await state.finish()
            await callback_etime_query.message.answer(
                f'Вы выбрали запись на корт с: {date_time["begin_time"]} по {date_time["end_time"]}',
                reply_markup=nav.RentMenu)
