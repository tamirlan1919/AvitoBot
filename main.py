import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from config import TOKEN
# Установите токен вашего бота
BOT_TOKEN = TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот. Как я могу вам помочь?")

# Обработка текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)