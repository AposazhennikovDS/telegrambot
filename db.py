import sqlite3

class BotDB:

    def __init__(self, db_file):
        # try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
        # except Exception:
        #     print("Ошибка при подключении к файлу базы данных", Exception)

    def add_user(self, chat_id):
        """Добавляем юзера в базу"""
        try:
            self.cursor.execute("INSERT INTO `users` (`chat_id`) VALUES (?)", (chat_id,))
            return self.conn.commit()
        except:
            # print("Ошибка при добавлении пользователя в бд")
            pass


    def user_exists(self, chat_id):
        """Проверяем, есть ли юзер в базе"""
        try:
            result = self.cursor.execute("SELECT `id` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            return bool(len(result.fetchall()))
        except Exception:
            # print("Ошибка при проверки наличия пользователя в бд", Exception)
            pass




    # def set_nickname(self, chat_id, nickname):
    #     """Добавляем ник в базу"""
    #     with self.conn:
    #         return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `chat_id` = ?", (nickname, chat_id,))

    def set_db_args(self, chat_id, **kwargs):
        """
        Добавляем любой(ые) элемент(ы) в таблицу users.
        Пример: set_args(chat_id, phone_number = data['phone_number], first_name = data[first_name'])
        """
        # try:
        with self.conn:
                for key, value in kwargs.items():
                    # print(key, value)
                    self.cursor.execute(f"UPDATE `users` SET `{key}` = ? WHERE `chat_id` = ?",(value, chat_id,))
                    self.conn.commit()
                return


    def get_db_args(self, chat_id, *args):
        """Получаем любой(ые) элемент(ы) из таблицы users"""
        data = dict()
        with self.conn:
            for key in args:
                    result = self.cursor.execute(f"SELECT `{key}` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchall()
                    for row in result:
                        data[key] = str(row[0])
            return data


    def get_user_id(self, chat_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `chat_id` = ?", (chat_id,))
        return result.fetchone()[0]

    def is_time_conflict(self, chat_id, date, time_begin, time_end):
        """" Проверяем предполагаемую бронь на конфликты с уже существующими"""
        try:
            result = self.cursor.execute(
                "SELECT count(*) FROM `reservation` where `date` = ? AND  `time_start` < ? AND `time_end` > ?",
                (date, time_end, time_begin,))

            if result[0] == 0:
                return False
            else:
                return True

        except Exception as e:
            # print(e)
            pass

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()