from money_cart import Authorize
import requests
TOKEN = '6515821471:AAFspRJMRcCFfJP8-g9WRGS02jK-aydFsBo'


YOOMONEY_CLIENT_ID = '201E4B97D576C7EABC93CDB031B24EB941B762922C037A226DC4124704A91333'
YOOMONEY_CLIENT_SECRET = 'E54A25F822D6788D8237BE72E97CA3E6F44F6C3D30E71377A921AD994BBF94D16C688AED27F8437EFAED5ACD503BE02C10989A124590F45D8CE20C13EAC16290'


# Запрос на обмен кода авторизации на токен доступа
response = requests.post('https://yoomoney.ru/oauth/authorize', data={
    'client_id': YOOMONEY_CLIENT_ID,
    'redirect_uri': 'https://t.me/aviitoo_bot',
    'response_type': 'code',
    'scope': ["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
})

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    print(f'Access Token: {access_token}')
else:
    print(f'Error: {response.status_code}')
    print(response.text)


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
        





