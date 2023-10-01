
import sqlite3
import datetime

def make_db():
    # Подключение к базе данных (если она существует) или создание новой
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # SQL-запрос для создания таблицы clients
    create_clients_table_query = '''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_telegram INTEGER,
        referral_link TEXT,
        frequently_asked_questions_triggers TEXT,
        premium_status INTEGER,
        payment_link TEXT,
        test_period_end TEXT
    );
    '''

    # SQL-запрос для создания таблицы chats
    create_chats_table_query = '''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        acc_id INTEGER,
        client_id TEXT,
        client_secret TEXT,
        test_period TEXT,
        FOREIGN KEY (acc_id) REFERENCES clients (id)

    );
    '''

    # Выполнение SQL-запросов для создания таблиц
    cursor.execute(create_clients_table_query)
    cursor.execute(create_chats_table_query)

    # Сохранение изменений в базе данных
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()






def get_clinet_id(idd):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id
    target_id_telegram = idd # Замените этим вашим id_telegram

        # SQL-запрос для выбора client_id по id_telegram
    select_query = 'SELECT client_id FROM clients WHERE id_telegram = ?'
    cursor.execute(select_query, (target_id_telegram,))

        # Извлечение результата запроса
    result = cursor.fetchone()

        # Если результат не равен None, то есть запись найдена, получите client_id
    if result is not None:
        client_id = result[0]
        print(f"client_id для id_telegram {target_id_telegram}: {client_id}")
        conn.close()
        return client_id

    else:
        print(f"Запись для id_telegram {target_id_telegram} не найдена")
        conn.close()
        return None

        # Закрытие соединения с базой данных


def get_token(idd):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id
    target_id_telegram = idd # Замените этим вашим id_telegram

        # SQL-запрос для выбора client_id по id_telegram
    select_query = 'SELECT token FROM clients WHERE id_telegram = ?'
    cursor.execute(select_query, (target_id_telegram,))

        # Извлечение результата запроса
    result = cursor.fetchone()

        # Если результат не равен None, то есть запись найдена, получите client_id
    if result is not None:
        token = result[0]
        print(f"token для id_telegram {target_id_telegram}: {token}")
        conn.close()
        return token

    else:
       

        print(f"Запись для id_telegram {target_id_telegram} не найдена")
        conn.close()
        return None

        # Закрытие соединения с базой данных



# Функция для получения даты окончания подписки из базы данных
def get_subscription_end_date_from_database(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT test_period_end FROM clients WHERE id_telegram = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S.%f')
    return None


# Функция для обновления даты окончания подписки в базе данных
def update_subscription_end_date_in_database(user_id, new_end_date):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE chats SET test_period = ? WHERE chat_id = ?', (new_end_date, user_id))
    conn.commit()
    conn.close()
