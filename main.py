import json
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import re
import sqlite3
import aiogram
from aiogram import executor
import datetime
from aiogram.types import Message
import asyncio
from contol import *
from avito_api import *
from aiogram.utils import markdown
from clean import *
import threading
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from state import *
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импортируем MemoryStorage
from aiogram.utils import executor
from aiogram.utils import markdown as md
from aiogram.utils import executor
from aiogram import executor


# Ваш токен Telegram-бота
BOT_TOKEN = '6515821471:AAFspRJMRcCFfJP8-g9WRGS02jK-aydFsBo'



# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
memory_storage = MemoryStorage()  # Инициализируем MemoryStorage
dp = Dispatcher(bot,storage=memory_storage)
dp.middleware.setup(LoggingMiddleware())
current_page = 0
current_page_message_id = None  # Инициализация переменной


current_page2 = 0
current_page_message_id2 = None

# Создаем множество для хранения уникальных имен пользователей
unique_user_names = set()


async def check_new_messages(message:types.Message):
    print('dooooneeeee')
    while True:
        # Здесь вы можете добавить логику для проверки наличия новых сообщений.
        user_id = get_clinet_id(message.chat.id)
        token = get_token(message.chat.id)
        avito_data = get_avito_unread_data(token=token, user_id=user_id)
        
        if avito_data and 'users' in avito_data:
            new_message_count = len(avito_data['users'])
            if new_message_count > 0:
                # Если есть новые сообщения, выполните необходимые действия,
                # например, уведомьте администратора или обработайте их.
                await bot.send_message(message.chat.id, f'Новых сообщений: {new_message_count}')
        
        await asyncio.sleep(10)  # Подождите 10 секунд перед следующей проверкой (или укажите другой интервал)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id,'Отправь мне Client ID своего Avito: ')



@dp.message_handler(commands='unread')
async def unread_data(message: types.Message):
    print(message)
    global current_page2
    global current_page_message_id2
    # Define the number of contacts to display per page
    contacts_per_page = 6
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    # Clear the unique_user_names set for the current page
    unique_user_names.clear()
    user_id = get_clinet_id(message.chat.id)
    token = get_token(message.chat.id)
    avito_data = get_avito_unread_data(token=token,user_id=user_id)

    if avito_data:
        user_data_list = []

        for chat in avito_data["chats"]:
            for user in chat["users"]:
                user_name = user["name"]
                user_id = user['id']  # Получаем user_id, если он существует, иначе пустая строка
                chat_id = chat["id"]
                
                # Проверяем, что имя пользователя уникально
                if user_name not in unique_user_names:
                    unique_user_names.add(user_name)
                    user_data_list.append({"user_id": user_id, "username": user_name, "chat_id": chat_id})

        # Define the number of contacts to display per page
        contacts_per_page = 6

        # Calculate the total number of pages
        total_pages = (len(user_data_list) + contacts_per_page - 1) // contacts_per_page

        # Check if the current page is out of bounds
        if current_page2 >= total_pages:
            current_page2 = 0

        # Calculate the start and end indices for slicing
        start_index = current_page2 * contacts_per_page
        end_index = (current_page2 + 1) * contacts_per_page

        # Get the contacts for the current page
        contacts_on_page = user_data_list[start_index:end_index]

        # Create a list of buttons for the contacts on the current page
        buttons = []
        for user_data in contacts_on_page:
            user_name = user_data["username"]
            cleaned_user_name = clean_callback_data(user_name)
            cleaned_user_name = cleaned_user_name[:64]
            cleaned_user_name+=' 👤'
            user_id = user_data["user_id"]
            chat_id = user_data["chat_id"]
            button = types.InlineKeyboardButton(text=cleaned_user_name, callback_data=f'unread_send^{cleaned_user_name}^{chat_id}^{user_id}')
            print(cleaned_user_name,chat_id,user_id)
            buttons.append(button)

        # Create the "Next" and "Back" buttons for page navigation
        navigation_buttons = []
        if total_pages > 1:
            if current_page2 > 0:
                navigation_buttons.append(types.InlineKeyboardButton(text="Back ⬅️", callback_data=f'unred_page_{current_page2 - 1}'))
            if current_page2 < total_pages - 1:
                navigation_buttons.append(types.InlineKeyboardButton(text="Next ➡️", callback_data=f'unread_page_{current_page2 + 1}'))

        # Add the navigation buttons to the keyboard
        if navigation_buttons:
            keyboard.add(*navigation_buttons)
        if buttons:
            keyboard.add(*buttons)

        # Check if there's an existing message to edit
        if current_page_message_id2:
            try:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=current_page_message_id2,
                                            text="Выберите пользователя:", reply_markup=keyboard)
            except aiogram.utils.exceptions.MessageNotModified:
                # Если сообщение не было изменено, просто пропустите ошибку
                pass
        else:
            # Send the initial message with the contacts and navigation buttons
            message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
            current_page_message_id2 = message.message_id

    else:
        await message.answer("Произошла ошибка при получении данных из Avito.")

@dp.message_handler(commands=['data'])
async def get_data(message: types.Message):
    print(message)
    global current_page
    global current_page_message_id
    # Define the number of contacts to display per page
    contacts_per_page = 6
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    # Clear the unique_user_names set for the current page
    unique_user_names.clear()
    user_id = get_clinet_id(message.chat.id)
    token = get_token(message.chat.id)
    avito_data = get_avito_data(token=token,user_id=user_id)

    if avito_data:
        user_data_list = []

        for chat in avito_data["chats"]:
            for user in chat["users"]:
                user_name = user["name"]
                user_id = user['id']  # Получаем user_id, если он существует, иначе пустая строка
                chat_id = chat["id"]
                
                # Проверяем, что имя пользователя уникально
                if user_name not in unique_user_names:
                    unique_user_names.add(user_name)
                    user_data_list.append({"user_id": user_id, "username": user_name, "chat_id": chat_id})

        # Define the number of contacts to display per page
        contacts_per_page = 6

        # Calculate the total number of pages
        total_pages = (len(user_data_list) + contacts_per_page - 1) // contacts_per_page

        # Check if the current page is out of bounds
        if current_page >= total_pages:
            current_page = 0

        # Calculate the start and end indices for slicing
        start_index = current_page * contacts_per_page
        end_index = (current_page + 1) * contacts_per_page

        # Get the contacts for the current page
        contacts_on_page = user_data_list[start_index:end_index]

        # Create a list of buttons for the contacts on the current page
        buttons = []
        for user_data in contacts_on_page:
            user_name = user_data["username"]
            cleaned_user_name = clean_callback_data(user_name)
            name = cleaned_user_name + ' 👤'

            user_id = user_data["user_id"]
            chat_id = user_data["chat_id"]
            button = types.InlineKeyboardButton(text=name, callback_data=f'send^{cleaned_user_name}^{chat_id}^{user_id}')
            print(cleaned_user_name,chat_id,user_id)
            buttons.append(button)

        # Create the "Next" and "Back" buttons for page navigation
        navigation_buttons = []
        if total_pages > 1:
            if current_page > 0:
                navigation_buttons.append(types.InlineKeyboardButton(text="Back ⬅️", callback_data=f'page_{current_page - 1}'))
            if current_page < total_pages - 1:
                navigation_buttons.append(types.InlineKeyboardButton(text="Next ➡️", callback_data=f'page_{current_page + 1}'))

        # Add the navigation buttons to the keyboard
        if navigation_buttons:
            keyboard.add(*navigation_buttons)
        if buttons:
            keyboard.add(*buttons)

        # Check if there's an existing message to edit
        if current_page_message_id:
            try:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=current_page_message_id,
                                            text="Выберите пользователя:", reply_markup=keyboard)
            except aiogram.utils.exceptions.MessageNotModified:
                # Если сообщение не было изменено, просто пропустите ошибку
                    # Если сообщение не было изменено, удаляем предыдущее сообщение и отправляем новое
                await bot.delete_message(chat_id=message.chat.id, message_id=current_page_message_id)
                message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
                current_page_message_id = message.message_id
        else:
            # Send the initial message with the contacts and navigation buttons
            message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
            current_page_message_id = message.message_id

    else:
        await message.answer("Произошла ошибка при получении данных из Avito.")




# Add a callback handler for page navigation
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('page_'))
async def page_navigation_callback(callback_query: types.CallbackQuery):
    global current_page  # Declare that we are using the global current_page variable
    global current_page_message_id  # Declare a global variable to store the message ID
    page_number = int(callback_query.data.split('_')[1])
    current_page = page_number  # Update the current page
    print(callback_query.message)
    # Trigger a refresh of the data
    await get_data(callback_query.message)


# Add a callback handler for page navigation
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('unread_page_'))
async def page_navigation_callback(callback_query: types.CallbackQuery):
    global current_page  # Declare that we are using the global current_page variable
    global current_page_message_id  # Declare a global variable to store the message ID
    page_number = int(callback_query.data.split('_')[1])
    current_page = page_number  # Update the current page
    print(callback_query.message)
    # Trigger a refresh of the data
    await get_data(callback_query.message)



# # Обработчик коллбэков от кнопок
# @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send_'))
# async def process_callback(callback_query: types.CallbackQuery):
#     user_name = callback_query.data.replace('send_', '')
#     await bot.send_message(callback_query.from_user.id, f"Вы выбрали пользователя: {user_name}")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('unread_send^'))
async def process_callback(callback_query: types.CallbackQuery):
    print(callback_query.data)
    user_data = callback_query.data.replace('send^', '').split('^')
    chat_id = ''
    user_id = ''
    if len(user_data)>2:
        chat_id, user_id = user_data[1], user_data[2]
    else:
        chat_id, user_id = user_data[0], user_data[1]
    # Создайте встроенную клавиатуру inline
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="💬Посмотреть чат", callback_data=f'view-chat^{chat_id}^{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message^{chat_id}^{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'back'))



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send^'))
async def process_callback(callback_query: types.CallbackQuery):
    print(callback_query.data)
    user_data = callback_query.data.replace('send^', '').split('^')
    chat_id = ''
    user_id = ''
    if len(user_data)>2:
        chat_id, user_id = user_data[1], user_data[2]
    else:
        chat_id, user_id = user_data[0], user_data[1]
    # Создайте встроенную клавиатуру inline
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="💬Посмотреть чат", callback_data=f'view-chat^{chat_id}^{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message^{chat_id}^{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'back'))


    # Отправьте сообщение с клавиатурой
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите действие:',
        reply_markup=keyboard
    )

    
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('seend^'))
async def process_callback2(callback_query: types.CallbackQuery):
    print(callback_query.data)
    user_data = callback_query.data.replace('send^', '').split('^')
    chat_id = ''
    user_id = ''
    if len(user_data)>2:
        chat_id, user_id = user_data[1], user_data[2]
    else:
        chat_id, user_id = user_data[0], user_data[1]
    # Создайте встроенную клавиатуру inline
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="💬Посмотреть чат", callback_data=f'view-chat^{chat_id}^{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message^{chat_id}^{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'back'))


    # Отправьте сообщение с клавиатурой
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите действие:',
        reply_markup=keyboard
    )


    
# Обработчик коллбэков от кнопок действий
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('back','view-chat^', 'send-message^', 'last-message^')))
async def action_callback(callback_query: types.CallbackQuery,state: FSMContext):
    action_data = callback_query.data
    print(action_data)
    action_data = callback_query.data.split('^')
    print(action_data)
    action = action_data[0]
    if len(action_data)>2:
        print(len(action_data))
        chat_id, user_id = action_data[1], action_data[2]
    else:
        pass

    if action == 'back':
        global current_page  # Declare that we are using the global current_page variable
        global current_page_message_id  # Declare a global variable to store the message ID
        callback_query.data = f'page_{current_page}'
        page_number = int(callback_query.data.split('_')[1])
        current_page = page_number  # Update the current page
        print(callback_query.message)
        # Trigger a refresh of the data
        await get_data(callback_query.message)

    elif action == 'view-chat':
        # Обработка действия "Посмотреть чат"
        resp = get_clinet_id(callback_query.message.chat.id)  # Получаем client_id
        token = get_token(callback_query.message.chat.id)
        data = get_avito_messages(user_id=resp, chat_id=chat_id, token=token)
        chat_text = ""
        messages = data['messages']  # Получаем все сообщения чата
        print(messages)

        # Итерируемся по сообщениям в обратном порядке
        for message in reversed(messages):
            message_type = message['type']
            sender = "<b>👤 Вы</b>" if message['direction'] == 'out' else "<b>📬 Вам</b>"

            if message_type == 'text':
                text = message['content']['text']
                created_timestamp = message['created']
                created_date = datetime.datetime.fromtimestamp(created_timestamp).strftime('%A %d %B')  # Форматируем дату как "понедельник 27 сентября"
                chat_text += f"{sender} ({created_date}): {text}\n\n"  # Добавляем имя отправителя и форматированную дату
            elif message_type == 'link':
                link_text = message['content']['link']['text']
                link_url = message['content']['link']['url']
                chat_text += f"{sender} ({created_date}) отправил ссылку: {link_text} ({link_url})\n"  # Добавляем имя отправителя и форматированную дату
            elif message_type == 'location':
                location_data = message['content']['location']
                location_text = location_data['text']
                location_title = location_data['title']
                location_lat = location_data['lat']
                location_lon = location_data['lon']
                chat_text += f"{sender} ({created_date}) отправил локацию:\n{location_text}\n({location_title}, Широта: {location_lat}, Долгота: {location_lon})\n"
            elif message_type == 'photo':
                # Обработка сообщений с фото
                chat_text += f"{sender} ({created_date}) отправил фотографию(и)\n"
            elif message_type == 'video':
                # Обработка сообщений с видео
                chat_text += f"{sender} ({created_date}) отправил видео\n"
            # Добавьте другие типы сообщений, такие как quick_reply и другие, по мере необходимости.

        token = get_token(callback_query.message.chat.id)

        mark_chat_as_read(resp, chat_id, token=token)
        # Отправляем объединенный текстовый чат
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message^{chat_id}^{user_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'send^{chat_id}^{user_id}'))
        await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=chat_text,
        parse_mode='html',
        reply_markup=keyboard
    )
        callback_query.data = f'send^{chat_id}^{user_id}'

        #await process_callback(callback_query=callback_query)

        # # Создаем одну строку, объединяя текст всех сообщений
        # chat_text = "\n".join([message['content']['text'] for message in data['messages']])

        # # Отправляем все сообщения одним сообщением
        # await bot.send_message(callback_query.from_user.id, f"Просмотр чата с пользователем: {user_name}\n\n{chat_text}")

    elif action == 'send-message':

    # Получаем chat_id и user_id из callback_data
        chat_id, user_id = action_data[1], action_data[2]

        # Запрашиваем текст у пользователя
        await bot.send_message(callback_query.from_user.id, "Введите текст сообщения:")

        # Устанавливаем состояние, чтобы ожидать ответа пользователя
        await MyStates.waiting_for_text.set()

        # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
        async with state.proxy() as data:
            data['chat_id'] = chat_id
            data['user_id'] = user_id

    #     # Send the message to the specified user
    #     resp1 = get_clinet_id(callback_query.message.chat.id)
    #     print(resp1)
    #     token = get_token(callback_query.message.chat.id)

    #     send_message(chat_id=chat_id, user_id=resp1, text='hello',token=token)
    #     mark_chat_as_read(resp, chat_id,token=token)

    #     # Notify the user that the message has been sent
    #     keyboard = types.InlineKeyboardMarkup(row_width=2)
    #     keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще", callback_data=f'send-message^{chat_id}^{user_id}'))
    #     keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'send^{chat_id}^{user_id}'))
    #     await bot.edit_message_text(
    #     chat_id=callback_query.message.chat.id,
    #     message_id=callback_query.message.message_id,
    #     text='Сообщение отправлено успешно!',
    #     parse_mode='html',
    #     reply_markup=keyboard
    # )

@dp.message_handler(state=MyStates.waiting_for_text)
async def process_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        user_id = data['user_id']

        # Отправляем текстовое сообщение пользователю
        resp = get_clinet_id(message.chat.id)  # Получаем client_id
        token = get_token(message.chat.id)
        send_message(chat_id=chat_id, user_id=resp, text=message.text, token=token)
        mark_chat_as_read(resp, chat_id, token=token)

        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-message^{chat_id}^{user_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{chat_id}^{user_id}'))
        # Уведомляем пользователя, что сообщение отправлено
        await bot.send_message(
            chat_id=message.chat.id,
            text='Сообщение отправлено успешно!',
            parse_mode='html',
            reply_markup= keyboard
        )

    # Завершаем состояние
    await state.finish()






# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    text = message.text

    if text.count(' ')==2:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        text = text.replace(' ','')
        print(text)
        # Данные пользователя
        id_telegram = message.chat.id  # Пример id_telegram
        client_id = get_clinet_id(message.chat.id)   # Пример client_id

        # SQL-запрос для проверки наличия записи с данным id_telegram
        select_query = 'SELECT * FROM clients WHERE id_telegram = ?'
        cursor.execute(select_query, (id_telegram,))

        # Извлечение результата запроса
        existing_record = cursor.fetchone()

        # Если запись существует, обновите её client_id
        if existing_record:
            print('попытка')
            update_query = 'UPDATE clients SET client_id = ? WHERE id_telegram = ?'
            cursor.execute(update_query, (text, id_telegram))
        else:
            # Если записи нет, создайте новую
            insert_query = 'INSERT INTO clients (id_telegram, client_id) VALUES (?, ?)'
            cursor.execute(insert_query, (id_telegram, client_id))

        # Сохранение изменений в базе данных
        conn.commit()

        # Закрытие соединения с базой данных
        conn.close()
    else:
        await bot.send_message(message.chat.id,'Ты написал</>')

    # Здесь вы можете обрабатывать текстовые сообщения от пользователя
    # и выполнять соответствующие действия

def run_check_new_messages():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_new_messages())

if __name__ == '__main__':
    make_db()
    executor.start_polling(dp, skip_updates=True)
    t = threading.Thread(target=run_check_new_messages)
    t.start()