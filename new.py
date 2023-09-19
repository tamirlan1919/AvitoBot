import requests
import json

url = "https://api.avito.ru/messenger/v2/accounts/14674344/chats/"
headers = {
    'Authorization': 'Bearer ZyWKvuGuStSnZbgzI2AtkAoYqMj58k96yhFsMyeI',
    'User-Agent': 'Python'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Use .json() method to get the JSON content
    data = response.json()

    # Now you can proceed to extract and process the JSON data
    chat_names = [chat["context"]["value"]["title"] for chat in data["chats"]]

    # Output chat names
    for name in chat_names:
        print(name)
else:
    print("Error:", response.json())
