
import requests
import json
import aiohttp


async def get_avito_data(token, user_id):
    url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/'
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def get_unread_messagef_avito(token, user_id):
    url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/?unread_only=true'
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def get_avito_unread_data(token, user_id):
    URL = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/'
    params = {
        'unread_only': 'true'  # Указываем, что нам нужны только непрочитанные чаты
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None
    

async def get_lst_messages_v3_async(token, user_id, chat_id):
    URL = f'https://api.avito.ru/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/'

    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def get_avito_messages(user_id, chat_id, token):
    url = f'https://api.avito.ru/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/'
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def send_message(user_id, chat_id, text, token):
    # Define the API endpoint URL
    url = f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages"

    # Define the headers, including the Authorization header with your API token
    headers = {
        'Authorization': f'Bearer {token}',
        "Content-Type": "application/json",  # Specify JSON content type
    }

    # Define the message data as a Python dictionary
    message_data = {
        "type": "text",
        "message": {
            "text": text
        }
    }

    # Convert the message data to JSON format
    json_data = json.dumps(message_data)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json_data) as response:
            if response.status == 200:
                print("Message sent successfully")
            else:
                print(f"Failed to send message. Status code: {response.status}")
                print(await response.text())  # Print the response content for debugging if needed



async def mark_chat_as_read(user_id, chat_id, token):
    # Define the API endpoint URL
    url = f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/read"

    # Define the headers, including the Authorization header with your API token
    headers = {
        'Authorization': f'Bearer {token}',
        "User-Agent": "Python",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                print("Chat marked as read successfully")
            else:
                print(f"Failed to mark chat as read. Status code: {response.status}")
                print(await response.text())  # Print the response content for debugging if needed


async def get_profile(token):
    # Define the API endpoint URL
    url = 'https://api.avito.ru/core/v1/accounts/self'

    # Define the headers, including the Authorization header with your API token
    headers = {
        'Authorization': f'Bearer {token}',
        "User-Agent": "Python",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None