import json
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

# Ваш токен Telegram-бота
BOT_TOKEN = '6515821471:AAFspRJMRcCFfJP8-g9WRGS02jK-aydFsBo'

# Ваш токен Avito API
AVITO_API_TOKEN = 'tUujJ7jCTRyPnaQrzfnOaQlL8hhQBBRxmx-oaYvw'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
from aiogram.utils import markdown

# URL для получения данных из API Avito
AVITO_API_URL = 'https://api.avito.ru/messenger/v2/accounts/147695266/chats/'

def get_avito_data():
    headers = {
        'Authorization': f'Bearer {AVITO_API_TOKEN}',
        'User-Agent': 'Python'
    }
    response = requests.get(AVITO_API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для доступа к данным из Avito. Введите /data, чтобы получить данные.")

@dp.message_handler(commands=['data'])
async def get_data(message: types.Message):
    avito_data = get_avito_data()

    if avito_data:
        all_user_names = []
        for chat in avito_data["chats"]:
            for user in chat["users"]:
                user_name = user["name"]
                all_user_names.append(user_name)
        
        # Отправить имена всех пользователей пользователю
        if all_user_names:
            await message.answer("\n".join(all_user_names))
        else:
            await message.answer("В чатах нет пользователей.")
    else:
        await message.answer("Произошла ошибка при получении данных из Avito.")


# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    text = message.text
    # Здесь вы можете обрабатывать текстовые сообщения от пользователя
    # и выполнять соответствующие действия

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)