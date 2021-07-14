import sqlite3


def is_message_user_hatelisted(user_id: int) -> bool:
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT count(user_id) FROM message_users WHERE user_id = %d" % user_id)
        result = c.fetchone()[0]
    c.close()
    conn.close()
    return result > 0


def insert_message_hatelist(user_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO message_users(user_id) VALUES (%d)" % user_id)
        conn.commit()
        print(f"Пользователь {user_id} добавлен в хейтлист")
    c.close()
    conn.close()


def delete_message_hatelist(user_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM message_users WHERE user_id=%d" % user_id)
        conn.commit()
        print(f"Пользователь {user_id} удален из хейтлиста")
    c.close()
    conn.close()


def get_all_message_users():
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM message_users")
        result = c.fetchall()
    c.close()
    conn.close()
    return result


def is_photo_user_hatelisted(user_id: int) -> bool:
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT count(user_id) FROM photo_users WHERE user_id = %d" % user_id)
        result = c.fetchone()[0]
    c.close()
    conn.close()
    return result > 0


def insert_photo_hatelist(user_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO photo_users(user_id) VALUES (%d)" % user_id)
        conn.commit()
        print(f"Пользователь {user_id} добавлен в хейтлист")
    c.close()
    conn.close()


def delete_photo_hatelist(user_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM photo_users WHERE user_id=%d" % user_id)
        conn.commit()
        print(f"Пользователь {user_id} удален из хейтлиста")
    c.close()
    conn.close()


def get_all_photo_users():
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM photo_users")
        result = c.fetchall()
    c.close()
    conn.close()
    return result


def set_message_cooldown(message_cooldown: int, type_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE settings SET message_cooldown = %d WHERE id = %d" % (message_cooldown, type_id))
        conn.commit()
        print(f"Задержка текста изменена на {message_cooldown} секунд")
    c.close()
    conn.close()


def set_photo_cooldown(photo_cooldown: int, type_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE settings SET photo_cooldown = %d WHERE id = %d" % (photo_cooldown, type_id))
        conn.commit()
        print(f"Задержка фото изменена на {photo_cooldown} секунд")
    c.close()
    conn.close()


def get_settings(type_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM settings WHERE id = %d" % type_id)
        result = c.fetchone()
    c.close()
    conn.close()
    return result
