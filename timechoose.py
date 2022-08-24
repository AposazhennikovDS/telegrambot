from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# setting callback_data prefix and parts
clock_callback = CallbackData('clock_callback', 'act', 'min')


class TimeChoose:
    async def start_clock(self) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """
        inline_kb = InlineKeyboardMarkup(row_width=4)

        # Calendar rows - Days of month
        time_in_day = [["8:00", "12:00", "16:00", "20:00"],
                       ["8:15", "12:15", "16:15", "20:15"],
                       ["8:30", "12:30", "16:30", "20:30"],
                       ["8:45", "12:45", "16:45", "20:45"],
                       ["9:00", "13:00", "17:00", "21:00"],
                       ["9:15", "13:15", "17:15", "21:15"],
                       ["9:30", "13:30", "17:30", "21:30"],
                       ["9:45", "13:45", "17:45", "21:45"],
                       ["10:00", "14:00", "18:00", "22:00"],
                       ["10:15", "14:15", "18:15", "22:15"],
                       ["10:30", "14:30", "18:30", "22:30"],
                       ["10:45", "14:45", "18:45", "22:45"],
                       ["11:00", "15:00", "19:00", "23:00"],
                       ["11:15", "15:15", "19:15", "23:15"],
                       ["11:30", "15:30", "19:30", "23:30"],
                       ["11:45", "15:45", "19:45", "23:45"]]
        for hour in time_in_day:
            inline_kb.row()
            for minutes in hour:
                inline_kb.insert(InlineKeyboardButton(str(minutes), callback_data=clock_callback.new("MIN", minutes)))

        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)

        if data['act'] == "MIN":
            await query.message.delete_reply_markup()  # removing inline keyboard
            return_data = True, str(data['min'])
        return return_data
