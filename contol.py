
import sqlite3
import datetime
import requests
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
        id_avito TEXT,
        client_id TEXT,
        client_secret TEXT,
        token TEXT,
        test_period TEXT,
        current_page INTEGER,
        current_page_message_id INTEGER,
        who_linked TEXT,
        link_rel TEXT,
        FOREIGN KEY (acc_id) REFERENCES clients (id)

    );
    '''
    create_msgs_table_query = '''
    CREATE TABLE IF NOT EXISTS msgs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        chat_id INTEGER UNIQUE,
        enabled INTEGER,
        week_days TEXT,
        avito_ids TEXT,
        response_text TEXT,
        FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
    );
    
    '''
    create_timemsgs_table_query = '''
    CREATE TABLE IF NOT EXISTS time_msgs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        chat_id INTEGER UNIQUE,
        enabled INTEGER,
        week_days TEXT,
        avito_ids TEXT,
        response_text TEXT,
        start_time TEXT,
        end_time TEXT,
        FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
    );
    
    '''
    create_auto_responses_table_query = '''
CREATE TABLE IF NOT EXISTS auto_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    trigger TEXT,
    enabled INTEGER,
    response_text TEXT,
    FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
);
'''
    create_check_work_msgs = '''
CREATE TABLE IF NOT EXISTS check_work_msgs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    week_days TEXT,
    avito_chat TEXT,
    response_text TEXT,
    FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
);
'''
    create_check_specific_msgs = '''
CREATE TABLE IF NOT EXISTS specific_msgs_time (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    time TEXT,
    avito_chat TEXT,
    response_text TEXT,
    FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
);
'''
    create_payment = '''
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    paysum REAL,
    procent REAL
);
'''
    cursor.execute(create_timemsgs_table_query)
    cursor.execute(create_clients_table_query)
    cursor.execute(create_payment)
    cursor.execute(create_chats_table_query)
    cursor.execute(create_msgs_table_query)
    cursor.execute(create_auto_responses_table_query)
    cursor.execute(create_check_work_msgs)
    cursor.execute(create_check_specific_msgs)
    # Сохранение изменений в базе данных
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()


def insert_initial_data():
    conn = sqlite3.connect('my_database.db')  # Замените 'my_database.db' на ваше имя базы данных
    cursor = conn.cursor()

    # Проверяем, пуста ли таблица "payment"
    cursor.execute("SELECT COUNT(*) FROM payment")
    count = cursor.fetchone()[0]

    if count == 0:
        # Если таблица пуста, вставляем начальные данные
        cursor.execute("INSERT INTO payment (telegram_id, paysum, procent) VALUES (1, 10.0, 20.0)")
        conn.commit()
        print("Начальные данные успешно вставлены.")
    else:
        print("Таблица уже содержит данные, начальные данные не вставляются.")

    conn.close()



def get_user_id(idd):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id
    target_id_telegram = idd # Замените этим вашим id_telegram

        # SQL-запрос для выбора client_id по id_telegram
    select_query = 'SELECT id_avito FROM chats WHERE chat_id = ?'
    cursor.execute(select_query, (target_id_telegram,))

        # Извлечение результата запроса
    result = cursor.fetchone()

        # Если результат не равен None, то есть запись найдена, получите client_id
    if result is not None:
        client_id = result[0]
        conn.close()
        return client_id

    else:
        conn.close()
        return None

        # Закрытие соединения с базой данных



def get_token(idd):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id
    target_id_telegram = idd # Замените этим вашим id_telegram

        # SQL-запрос для выбора client_id по id_telegram
    select_query = 'SELECT token FROM chats WHERE chat_id = ?'
    cursor.execute(select_query, (target_id_telegram,))

        # Извлечение результата запроса
    result = cursor.fetchone()

        # Если результат не равен None, то есть запись найдена, получите client_id
    if result is not None:
        token = result[0]
        conn.close()
        return token

    else:
       

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


def set_personal_token(client_id,client_secret):
    url = "https://api.avito.ru/token/"



    # Параметры запроса
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    # Отправляем POST-запрос
    response = requests.post(url, data=data)

    # Проверяем статус-код ответа
    if response.status_code == 200:
        # Получаем токен из ответа
        token_data = response.json()
        access_token = token_data.get("access_token")
        token_type = token_data.get("token_type")
        
        print("Access Token:", access_token)
        print("Token Type:", token_type)
        return access_token
    else:
        print("Ошибка при запросе токена. Код статуса:", response.status_code)
        print("Текст ошибки:", response.text)
        




def get_chats_with_data():
    conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    # Выполните SQL-запрос для извлечения чатов с заполненными данными
    cursor.execute('''
        SELECT chat_id
        FROM chats
        WHERE id_avito IS NOT NULL
          AND client_id IS NOT NULL
          AND client_secret IS NOT NULL
          AND token IS NOT NULL
    ''')

    chats_with_data = cursor.fetchall()

    conn.close()
    return chats_with_data



def get_chats_with_triggers():
    try:
        conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
        cursor = conn.cursor()

        # Выполните SQL-запрос для извлечения чатов с заполненными данными
        cursor.execute('''
            SELECT *
            FROM auto_responses
            WHERE trigger IS NOT NULL
            AND response_text IS NOT NULL

        ''')

        chats_with_data = cursor.fetchall()

        conn.close()
        return chats_with_data
    except:
        return None

def clear_check_work_msgs(id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM check_work_msgs WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def clear_specific_msgs_time(avito_chat):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM specific_msgs_time WHERE avito_chat = ?", (avito_chat,))
    conn.commit()
    conn.close()


def get_chats_with_msgs():
    conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    # Выполните SQL-запрос для извлечения чатов с заполненными данными
    cursor.execute('''
        SELECT *
        FROM msgs
        WHERE week_days IS NOT NULL
          AND response_text IS NOT NULL

    ''')

    chats_with_data = cursor.fetchall()

    conn.close()
    return chats_with_data


def get_time(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли значение в атрибуте "тестовый период" для данного пользователя
    cursor.execute('SELECT test_period FROM chats WHERE chat_id = ?', (user_id[0],))
    test_period_end = cursor.fetchone()
    # Здесь предполагается, что вы извлекли дату и время окончания подписки из базы данных
    subscription_end_time = ''
    try:
        subscription_end_time = datetime.datetime.strptime(test_period_end[0], '%Y-%m-%d %H:%M:%S.%f')
    except Exception as e:
        print('Error:', e)
    
    if subscription_end_time is None:
        return None
    
    current_time = datetime.datetime.now()
    if current_time <= subscription_end_time:
        return True
    else:
        return False

def get_time2(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли значение в атрибуте "тестовый период" для данного пользователя
    cursor.execute('SELECT test_period FROM chats WHERE chat_id = ?', (user_id,))
    test_period_end = cursor.fetchone()
    # Здесь предполагается, что вы извлекли дату и время окончания подписки из базы данных
    subscription_end_time = ''
    try:
        subscription_end_time = datetime.datetime.strptime(test_period_end[0], '%Y-%m-%d %H:%M:%S.%f')
    except Exception as e:
        print('Error:', e)
    
    if subscription_end_time is None:
        return None
    
    current_time = datetime.datetime.now()
    if current_time <= subscription_end_time:
        return True
    else:
        return False
    

def get_enabled_triggers(chat_id):
    conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    # Выполните SQL-запрос для извлечения чатов с заполненными данными
    cursor.execute('''
        SELECT enabled
        FROM auto_responses
        WHERE chat_id = ?

    ''', (chat_id,))

    data = cursor.fetchone()

    conn.close()
    return data


def get_enabled_msgs(chat_id):
    conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    # Выполните SQL-запрос для извлечения чатов с заполненными данными
    cursor.execute('''
        SELECT enabled
        FROM msgs
        WHERE chat_id = ?

    ''', (chat_id,))

    data = cursor.fetchone()

    conn.close()
    return data


def get_enabled_tme_msgs(chat_id):
    conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    # Выполните SQL-запрос для извлечения чатов с заполненными данными
    cursor.execute('''
        SELECT enabled
        FROM time_msgs
        WHERE chat_id = ?

    ''', (chat_id,))

    data = cursor.fetchone()

    conn.close()
    return data

def get_chats_with_time_msgs():
    conn = sqlite3.connect('my_database.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    # Выполните SQL-запрос для извлечения чатов с заполненными данными
    cursor.execute('''
        SELECT *
        FROM time_msgs
        WHERE week_days IS NOT NULL
          AND response_text IS NOT NULL
          AND start_time IS NOT NULL
          AND end_time IS NOT NULL
          AND avito_ids IS NOT NULL

    ''')

    chats_with_data = cursor.fetchall()

    conn.close()
    return chats_with_data

async def update_token_for_chat(chat_id,client_id,client_secret):
    # Здесь выполняется обновление токена для данного чата
    # Используйте API Avito для получения нового токена и обновите его в базе данных
    new_token = set_personal_token(client_id=client_id,client_secret=client_secret)
    print(new_token)
    # Обновите токен в базе данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET token = ? WHERE chat_id = ?", (new_token, chat_id))
    conn.commit()
    conn.close()



