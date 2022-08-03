from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from database import Base, async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result


class User(Base, ModelAdmin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # id человека с которым чат ведет переписку(например 338303820)
    first_name = Column(String,
                        # nullable=False
                        )  # Имя
    last_name = Column(String,
                       # nullable=False
                       )  # Фамилия (Иванов)
    phone_number = Column(Integer,
                          # nullable=False
                          )  # телефон в формате 7XXXXXXXX(здесь нужны будут регулярные выражения)
    join_date = Column(DateTime,
                       # nullable=False
                       )  # дата регистрации в формате dd.mm.yyyy hh:mm
    reservations = relationship("Reservation")

    # required in order to access columns with server defaults
    # or SQL expression defaults, after a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"phone_number={self.phone_number}, "
            f"join_date={self.join_date}, "
            f")>"
        )


class Reservation(Base, ModelAdmin):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))  # id человека с которым чат ведет переписку(например 338303820)
    date = Column(DateTime, nullable=False)  # дата на которую бронируем в формате dd.mm.yyyy
    time_start = Column(DateTime, nullable=False)  # время начала брони в формате hh:mm
    time_end = Column(DateTime, nullable=False)  # время окончания брони в формате hh:mm
    duration = Column(DateTime, nullable=False)  # длительность брони в формате минут
    court_id = Column(Integer, nullable=False)  # номер корта 1/2
    count = Column(Integer, nullable=False)  # количество участников тренировки
    type = Column(Integer, nullable=False)  # тип тренировки(открытая/закрытая)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(" f"id={self.id}, " f"date={self.date}" f")>"
        )

    @classmethod
    async def filter_by_user_id(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        posts = await async_db_session.execute(query)
        return posts.scalars().all()