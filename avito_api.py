
import requests
import json



def get_avito_data(token,user_id):
    AVITO_API_URL = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/' # URL для получения данных из API Avito

    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }
    response = requests.get(AVITO_API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None




def get_avito_unread_data(token, user_id):
    URL = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats/'
    params = {
        'unread_only': 'true'  # Указываем, что нам нужны только непрочитанные чаты
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }
    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    

def get_avito_messages(user_id,chat_id,token):
    URL = f'https://api.avito.ru/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/'
    print(URL)
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }
    response = requests.get(URL, headers=headers)
  
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    

def send_message(user_id,chat_id,text,token):
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
            "text": f"{text}"
        }
    }

    # Convert the message data to JSON format
    json_data = json.dumps(message_data)
    print(url)
    # Send the POST request with data in the request body
    response = requests.post(url, headers=headers, data=json_data)

    # Check the response status code and content
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging if needed




def mark_chat_as_read(user_id, chat_id,token):
    URL = f'https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/read'
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python'
    }
    response = requests.post(URL, headers=headers)
    
    if response.status_code == 200:
        print("Chat marked as read successfully")
    else:
        print(f"Failed to mark chat as read. Status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging if needed

