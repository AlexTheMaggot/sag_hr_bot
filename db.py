import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


def user_create(user_id):
    cursor.execute(f'''INSERT INTO users (user_id) VALUES ({user_id})''')
    conn.commit()


def user_get_detail(user_id):
    fetch = cursor.execute(f'''SELECT * FROM users WHERE user_id = {user_id}''').fetchone()
    user = {
        'user_id': fetch[0],
        'lang': fetch[1],
        'name': fetch[2],
    }
    return user


def user_update(user_id, lang=None, name=None):
    if lang:
        cursor.execute(f'''UPDATE users SET lang = '{lang}' ''')
        conn.commit()
    if name:
        cursor.execute(f'''UPDATE users SET name = '{name}' ''')
        conn.commit()
