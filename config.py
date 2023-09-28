from yoomoney import Authorize
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