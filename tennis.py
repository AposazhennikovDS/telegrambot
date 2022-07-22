import sqlite3


try:
    conn = sqlite3.connect("tennisdb.db")
    cursor = conn.cursor()

    #Создаем пользователя с user_id = 1000
    cursor.execute("INSERT OR IGNORE INTO 'users' ('USER_ID') VALUES (?)", (1000,))
    # Считываем всех пользователей
    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())

    #Подтверждаем изменения
    conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if(conn):
        conn.close()