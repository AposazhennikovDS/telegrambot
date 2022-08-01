import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def add_user(self, chat_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`chat_id`) VALUES (?)", (chat_id,))
        return self.conn.commit()

    def user_exists(self, chat_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `chat_id` = ?", (chat_id,))
        return bool(len(result.fetchall()))

    # def set_nickname(self, chat_id, nickname):
    #     """Добавляем ник в базу"""
    #     with self.conn:
    #         return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `chat_id` = ?", (nickname, chat_id,))

    def set_phone_number(self, chat_id, phone_number):
        """Добавляем номер телефона в базу"""
        with self.conn:
            return self.cursor.execute("UPDATE `users` SET `phone_number` = ? WHERE `chat_id` = ?", (phone_number, chat_id,))

    def set_first_name(self, chat_id, first_name):
        """Добавляем ИМЯ"""
        with self.conn:
            return self.cursor.execute("UPDATE `users` SET `first_name` = ? WHERE `chat_id` = ?", (first_name, chat_id,))

    def get_first_name(self, chat_id):
        """Получаем Имя из БД"""
        with self.conn:
            result = self.cursor.execute("SELECT `first_name` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchall()
            for row in result:
                first_name = str(row[0])
            return first_name

    def get_last_name(self, chat_id):
        """Получаем Фамилию из БД"""
        with self.conn:
            result = self.cursor.execute("SELECT `last_name` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchall()
            for row in result:
                last_name = str(row[0])
            return last_name

    def get_phone_number(self, chat_id):
        """Получаем номер телефона из БД"""
        with self.conn:
            result = self.cursor.execute("SELECT `phone_number` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchall()
            for row in result:
                phone_number = str(row[0])
            return phone_number

    def set_last_name(self, chat_id, last_name):
        """Добавляем ФАМИЛИЮ"""
        with self.conn:
            return self.cursor.execute("UPDATE `users` SET `last_name` = ? WHERE `chat_id` = ?", (last_name, chat_id,))

    def get_signup(self, chat_id):
        """Получаем статус регистрации"""
        with self.conn:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup


    def set_signup(self, chat_id, signup):
        """Меняем статус регистрации"""
        with self.conn:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `chat_id` = ?", (signup, chat_id,))



    def get_user_id(self, chat_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `chat_id` = ?", (chat_id,))
        return result.fetchone()[0]

    
    def is_time_conflict(self, chat_id, date, time_begin, time_end):
        """" проверяем предполагаемую бронь на конфликты с уже существующими"""
        try:    
            result = self.cursor.execute("SELECT count(*) FROM `reservation` where `date` = ? AND  `time_start` < ? AND `time_end` > ?",
                                         (date, time_end, time_begin,))
        
            if (result[0] == 0):
                return False
            else:
                return True
        
        except Exception as e:
            print(e)

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
