
import sqlite3


def make_db():
        # Подключение к базе данных (если она существует) или создание новой
    conn = sqlite3.connect('my_database.db')

    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # SQL-запрос для создания таблицы
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_telegram INTEGER,
        client_id INTEGER
    );
    '''

    # Выполнение SQL-запроса для создания таблицы
    cursor.execute(create_table_query)
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



  