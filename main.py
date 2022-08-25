from aiogram.utils import executor


if __name__ == '__main__':
    from handlers.registration.start import *
    executor.start_polling(dp, skip_updates=True)
