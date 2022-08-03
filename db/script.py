import asyncio

from database import async_db_session
from models import Reservation, User


async def init_db():
    await async_db_session.init()
    await async_db_session.create_all()


async def add_user(tg_id: int, **kwargs) -> User:
    """Добавляем юзера в базу"""
    await User.create(id=tg_id, **kwargs)
    user = await User.get(id=tg_id)
    return user


async def is_user_exists(tg_id: int) -> bool:
    """Проверяем, есть ли юзер в базе"""
    try:
        user = await User.get(id=tg_id)
        return True
    except:
        return False


async def create_reservation(user_id):
    await Reservation.create(user_id=user_id)
    reservations = await Reservation.filter_by_user_id(user_id)
    return reservations


async def set_phone_number(tg_id: int, phone_number: int) -> None:
    """Добавляем номер телефона в базу"""
    await User.update(id=tg_id, phone_number=phone_number)


async def set_first_name(tg_id: int, first_name: str) -> None:
    """Добавляем имя в базу"""
    await User.update(id=tg_id, first_name=first_name)


async def update_user(id, first_name):
    await User.update(id, first_name=first_name)
    user = await User.get(id)
    return user.full_name


async def async_main_test():
    # протестируем всё и вся
    await init_db()
    print(await add_user(123456, first_name='Иван', last_name='Петров'))
    print(await is_user_exists(123456))
    print(await is_user_exists(1234567))
    await set_phone_number(123456, 9999999)
    await set_first_name(123456, first_name='Петя')


if __name__ == '__main__':
    asyncio.run(async_main_test())