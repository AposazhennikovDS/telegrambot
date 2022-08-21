import calendar
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery





# setting callback_data prefix and parts
time_callback = CallbackData('time', 'choose time', 'clock', 'o`clock')


class SimpleTime:






    async def start_time(self) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided time
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """
        inline_kb = InlineKeyboardMarkup(row_width=4)
        ignore_callback = time_callback.new("IGNORE", 0)  # for buttons with no answer
        # Time rows - Time from 00:00 to 23:45 with 15 min interval
        page = list()
        def add_to_list_time(begin_n, end_n, list_name):
            for i in range(begin_n, end_n):
                list_name.append([f"{i}:00", f"{i + 2}:00", f"{i + 4}:00", f"{i + 6}:00"])
                list_name.append([f"{i}:15", f"{i + 2}:15", f"{i + 4}:15", f"{i + 6}:15"])
                list_name.append([f"{i}:30", f"{i + 2}:30", f"{i + 4}:30", f"{i + 6}:30"])
                list_name.append([f"{i}:45", f"{i + 2}:45", f"{i + 4}:45", f"{i + 6}:45"])
        # Time rows - Time from 00:00 to 23:45 with 15 min interval 3 pages
        add_to_list_time(0, 2, page)
        for Time in page:
            inline_kb.row()
            for clock in Time:
                if(Time == 0):
                    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(str(Time), callback_data=time_callback.new("TIME")))


        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        """

        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by time_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """

        page = list()
        def add_to_list_time(begin_n, end_n, list_name):
            for i in range(begin_n, end_n):
                list_name.append([f"{i}:00", f"{i + 2}:00", f"{i + 4}:00", f"{i + 6}:00"])
                list_name.append([f"{i}:15", f"{i + 2}:15", f"{i + 4}:15", f"{i + 6}:15"])
                list_name.append([f"{i}:30", f"{i + 2}:30", f"{i + 4}:30", f"{i + 6}:30"])
                list_name.append([f"{i}:45", f"{i + 2}:45", f"{i + 4}:45", f"{i + 6}:45"])

        return_data = (False, None)
        temp_date = add_to_list_time(0, 2, page)
        # processing empty buttons, answering with no action
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        # user picked a day button, return date
        if data['act'] == "TIME":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, int(data['time'])
        # user navigates to previous page, editing message with new time
        if data['act'] == "PREV-PAGE":
            prev_date = add_to_list_time(0, 2, page)
            await query.message.edit_reply_markup(await self.start_calendar(int(prev_date.year), int(prev_date.month)))
        # user navigates to next year, editing message with new calendar
        if data['act'] == "NEXT-PAGE":
            next_date = temp_date + timedelta(days=365)
            await query.message.edit_reply_markup(await self.start_calendar(int(next_date.year), int(next_date.month)))
        # user navigates to previous month, editing message with new calendar
        if data['act'] == "PREV-MONTH":
            prev_date = temp_date - timedelta(days=1)
            await query.message.edit_reply_markup(await self.start_calendar(int(prev_date.year), int(prev_date.month)))
        # user navigates to next month, editing message with new calendar
        if data['act'] == "NEXT-MONTH":
            next_date = temp_date + timedelta(days=31)
            await query.message.edit_reply_markup(await self.start_calendar(int(next_date.year), int(next_date.month)))
        # at some point user clicks DAY button, returning date
        return return_data
