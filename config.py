import requests
from contol import *
from avito_api import *
TOKEN = '6515821471:AAFspRJMRcCFfJP8-g9WRGS02jK-aydFsBo'

admin_ids = [5455171373,1616187,907703822,782280769]
comms = ['/start','/data','/account_info']

YOOMONEY_CLIENT_ID = '201E4B97D576C7EABC93CDB031B24EB941B762922C037A226DC4124704A91333'
YOOMONEY_CLIENT_SECRET = 'E54A25F822D6788D8237BE72E97CA3E6F44F6C3D30E71377A921AD994BBF94D16C688AED27F8437EFAED5ACD503BE02C10989A124590F45D8CE20C13EAC16290'


# # Запрос на обмен кода авторизации на токен доступа
# response = requests.post('https://yoomoney.ru/oauth/authorize', data={
#     'client_id': YOOMONEY_CLIENT_ID,
#     'redirect_uri': 'https://t.me/aviitoo_bot',
#     'response_type': 'code',
#     'scope': ["account-info",
#              "operation-history",
#              "operation-details",
#              "incoming-transfers",
#              "payment-p2p",
#              "payment-shop",
#              ]
# })

# if response.status_code == 200:
#     token_data = response.json()
#     access_token = token_data['access_token']
#     print(f'Access Token: {access_token}')
# else:
#     print(f'Error: {response.status_code}')
#     print(response.text)


async def get_unread_messages_trig(chat_id):
    avito_id = get_user_id(chat_id)  # Замените этот код на получение id пользователя из вашей базы данных
    token = get_token(chat_id)  # Замените этот код на получение токена из вашей базы данных

    # Используйте API Avito для получения непрочитанных сообщений
    json_data = get_unread_messagef_avito(token=token, user_id=avito_id)  

    unread_messages = []
    if "chats" in json_data:
        for chat in json_data["chats"]:
            message_text = chat["last_message"]["content"]["text"]
            chat_id = chat["id"]
            unread_messages.append({"chat_id": chat_id, "text": message_text})

    return unread_messages
    # Ваш код для получения непрочитанных сообщений из Avito
    # Используйте API для получения сообщений



import sqlite3

def find_matching_trigger(user_text):
    try:
        conn = sqlite3.connect('my_database.db')  # Replace with your database name
        cursor = conn.cursor()

        # Execute SQL query to retrieve all triggers from the database
        cursor.execute("SELECT trigger, response_text FROM auto_responses")
        all_triggers = cursor.fetchall()

        cleaned_user_text = user_text.lower().strip()

        best_trigger = None
        best_response_text = None
        max_match_length = 0

        for trigger, response_text in all_triggers:
            cleaned_trigger = trigger.lower().strip()

            # Check if any trigger word is in the user's text
            if any(word in cleaned_user_text for word in cleaned_trigger.split()):
                match_length = len(cleaned_trigger)
                if match_length > max_match_length:
                    max_match_length = match_length
                    best_trigger = trigger
                    best_response_text = response_text

        if best_trigger:
            print(best_trigger, best_response_text)
            return best_trigger, best_response_text

    except Exception as e:
        print(f"Error in find_matching_trigger: {e}")
    finally:
        conn.close()

    return None, None


def find_matching_answer():
    try:
        conn = sqlite3.connect('my_database.db')  # Замените на имя вашей базы данных
        cursor = conn.cursor()
        lst = []
        # Выполните SQL-запрос для получения всех триггеров из базы данных
        cursor.execute("SELECT week_days, response_text FROM msgs")
        all_triggers = cursor.fetchall()

        if all_triggers:
            return all_triggers
        else:
            return None
    


    except Exception as e:
        print(f"Error in find_matching_trigger: {e}")
    finally:
        conn.close()

    return None, None


def find_matching_answer_work():
    try:
        conn = sqlite3.connect('my_database.db')  # Замените на имя вашей базы данных
        cursor = conn.cursor()
        lst = []
        # Выполните SQL-запрос для получения всех триггеров из базы данных
        cursor.execute("SELECT week_days, response_text FROM time_msgs")
        all_triggers = cursor.fetchall()

        if all_triggers:
            return all_triggers
        else:
            return None
    


    except Exception as e:
        print(f"Error in find_matching_trigger: {e}")
    finally:
        conn.close()

    return None, None

async def send_auto_response(token,chat_id,user_id, response):
    # Define the API endpoint URL
    url = f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages"

    # Define the headers, including the Authorization header with your API token
    headers = {
        'Authorization': f'Bearer {token}',
        "Content-Type": "application/json",  # Specify JSON content type
    }

    # Define the data to be sent in the request body as a Python dictionary
    message_data = {
        "type": "text",
        "message": {
            "text": f"{response}"
        }
    }
    # Ваш код для отправки автоматического ответа в чат с указанным chat_id
    # Используйте API Avito для отправки сообщения








