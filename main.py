from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import sqlite3
import aiogram
from aiogram import executor
import datetime
from aiogram.types import Message
import asyncio
from contol import *
from avito_api import *
from math import ceil
from aiogram.utils import markdown
from clean import *
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
from yoomoney import Client
import os
from aiogram import types
from aiogram.utils import exceptions
from money_cart import get_sum
from teext import *
from config import *
from aiogram.dispatcher.filters import Command, ChatTypeFilter
yoomoney_token = "4100117394518969.25C11A278171A9D98CF57B29E20869FE7175F8E5F0D82C642CB12B819214769229B792D693CD7A205D5D8B524294B1E710CECA73FB581A110CD748405B3A3709592F767FB683ACCE256C92453C4EA831F0E9EBA02063DF8DBA8728EE9B2A2CC60AA1EAD2AF79160F273D90F23C06E6E66B7B874261A33FD1BBA66C0A96297EAD"

client = Client(yoomoney_token)
# Ваш токен Telegram-бота
BOT_TOKEN = '6657768547:AAE4-RHRZtnIJ6lumQVqBrvmP7tUsvVFhG8'

users_per_page_2 = 3
current_page_2 = 1
total_pages_2 = 1

week_days_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

day_mapping = {
    'MON': 'ПН',
    'TUE': 'ВТ',
    'WED': 'СР',
    'THU': 'ЧТ',
    'FRI': 'ПТ',
    'SAT': 'СБ',
    'SUN': 'ВС'
}

selected_days_dict ={}


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN,disable_web_page_preview=True)

memory_storage = MemoryStorage()  # Инициализируем MemoryStorage
dp = Dispatcher(bot,storage=memory_storage)
dp.middleware.setup(LoggingMiddleware())
sent_messages = {}
sent_welcome_messages = {}






# Создаем множество для хранения уникальных имен пользователей
unique_user_names = set()
image_folder = 'images/test_period'
image_folder2 = 'images/bot'
image_folder3 = 'images/to_answer'
image_folder4 = 'images/to_show'
image_folder5 = 'images/data'


async def check_new_messages(message: types.Message):
    while True:
        try:
            # Здесь вы можете добавить логику для проверки наличия новых сообщений.
            user_id = get_user_id(message.chat.id)
            token = get_token(message.chat.id)
            avito_data = await get_avito_unread_data(token=token, user_id=user_id)

            if avito_data and 'users' in avito_data:
                new_message_count = len(avito_data['users'])
                if new_message_count > 0:
                    # Если есть новые сообщения, выполните необходимые действия,
                    # например, уведомьте администратора или обработайте их.
                    await bot.send_message(message.chat.id, f'Новых сообщений: {new_message_count}')

        except Exception as e:
            # Здесь вы можете обработать исключение, например, залогировать его или отправить уведомление.
            pass
        await asyncio.sleep(10)  # Подождите 10 секунд перед следующей проверкой (или укажите другой интервал)


@dp.message_handler(Command("start") & ChatTypeFilter(types.ChatType.PRIVATE))
async def start(message: types.Message):
    text = start_text
    await bot.send_message(message.chat.id,text=text,parse_mode='html')
    with open('video.gif', 'rb') as video_file:
        await bot.send_video(chat_id=message.chat.id, video=video_file)
    text1 = instruct_first
    user_id = message.chat.id
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    row = ''
    try:
        cursor.execute('SELECT * FROM clients WHERE id_telegram = ?', (user_id,))
        row = cursor.fetchone()  # Получаем первую найденную запись
    except Exception as e:
        print("Error:", e)
        row = None
    if row is None:
        cursor.execute('INSERT INTO clients (id_telegram) VALUES (?)', (user_id,))
        conn.commit()  # Сохраняем изменения в базе данных
    else:
        pass

    # Создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    print(message.chat.id,type(message.chat.id))
    if message.chat.id in admin_ids:
        keyboard.add(
            types.InlineKeyboardButton(text='🎥 Видео', callback_data='video'),
            types.InlineKeyboardButton(text='📋 Список аккаунтов', callback_data='spisok')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='🤖 Автоответы', callback_data='auto_answera'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='sos')
    )
        keyboard.add(types.InlineKeyboardButton(text='Админ панель',callback_data='acc_back'))
    else:
        keyboard.add(
            types.InlineKeyboardButton(text='🎥 Видео', callback_data='video'),
            types.InlineKeyboardButton(text='📋 Список аккаунтов', callback_data='spisok')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='🤖 Автоответы', callback_data='auto_answera'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='sos')
    )
    try:

        # Проверяем, есть ли значение в атрибуте "тестовый период" для данного пользователя
        cursor.execute('SELECT test_period_end FROM clients WHERE id_telegram = ?', (user_id,))
        test_period_end = cursor.fetchone()
        if test_period_end[0] is None:
            # Если значение "тестовый период" отсутствует, добавляем кнопку "тестовый период" в клавиатуру
            keyboard.add(types.InlineKeyboardButton(text='🕒 Тестовый период', callback_data='test_period_start'))
    except:
        pass
    conn.close()


    await bot.send_message(message.chat.id, text=text1,reply_markup=keyboard,parse_mode='html')

@dp.message_handler(Command("start") & ChatTypeFilter(types.ChatType.GROUP))
async def start_group(message: types.Message):
    chat_id = message.chat.id
    user_id_telegram = message.from_user.id
    # Вставляем запись в таблицу chats
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    print('что таке')
    try:
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Check if the test_period exists in the clients table
            cursor.execute('SELECT test_period_end FROM clients WHERE id = ?', (user_id[0],))
            test_per = cursor.fetchone()
            print(test_per)
            if test_per[0] is not None:
                # Проверяем, существует ли запись с такими acc_id и chat_id
                cursor.execute('SELECT id FROM chats WHERE acc_id = ? AND chat_id = ?', (user_id[0], chat_id))
                existing_chat = cursor.fetchone()
                print('зашел')
                print(existing_chat)
                if not existing_chat:
                    print('не зашел')
                    # Если запись не существует, вставляем новую запись в таблицу chats
                    cursor.execute('INSERT INTO chats (chat_id, acc_id, test_period, link_rel) VALUES (?, ?, ?, ?)', (chat_id, user_id[0], test_per[0], message.chat.id))
                    conn.commit()
                    text1 = before_reading
                    await bot.send_message(message.chat.id,'🎉 Добро пожаловать в наш бот! 🤖')
                    #await bot.send_message(message.chat.id,text='text1')
                    with open('video2.mp4', 'rb') as video_file:
                        await bot.send_video(chat_id=message.chat.id, video=video_file)    
                    text2 = instruct_second
                    
                    await bot.send_message(message.chat.id,text=text2,parse_mode='html')
                    with open('video3.mp4', 'rb') as video_file:
                        await bot.send_video(chat_id=message.chat.id, video=video_file)    

                    text3 = instruct_third
                    await bot.send_message(message.chat.id,text=text3)
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text='📋 Проверить статус подписки',callback_data='check_vip'))
                    keyboard.add(types.InlineKeyboardButton(text='💳 Проверить платежи', callback_data='check_money'))
                    keyboard.add(types.InlineKeyboardButton(text='➕ Подключить аккаунт',callback_data='check_connection'))
                    keyboard.add(types.InlineKeyboardButton(text='🔌 Реф ссылка',callback_data='check_ref'))

                    await bot.send_message(message.chat.id,text='Выберите опцию',reply_markup=keyboard)
                else:
                    pass
            else:
                # Send an alert message to the user to connect a test period
                await bot.send_message(message.chat.id, 'Пожалуйста подключите тестовый период в группе')
    except:
        pass

    conn.close()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_vip')
async def check_vip(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    user_id = callback_query.message.chat.id
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли значение в атрибуте "тестовый период" для данного пользователя

    # Здесь предполагается, что вы извлекли дату и время окончания подписки из базы данных
    cursor.execute('SELECT test_period FROM chats WHERE chat_id = ?', (user_id,))
    test_period_end = cursor.fetchone()
    subscription_end_time = ''
    try:

        subscription_end_time = datetime.datetime.strptime(test_period_end[0], '%Y-%m-%d %H:%M:%S.%f')
    except Exception as e:
        print('Error:', e)
    
    if subscription_end_time is None:
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.send_message(callback_query.message.chat.id, "У вас нет активной подписки. Хотите приобрести подписку?",reply_markup=keyboard)
        return


    
    current_time = datetime.datetime.now()
    if current_time >= subscription_end_time:
        try:
            # Попробуйте удалить предыдущее сообщение с клавиатурой
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        except exceptions.MessageToDeleteNotFound:
            pass  # Сообщение уже удалено или не существует
        
        # Здесь можете отправить клавиатуру с кнопкой для покупки подписки
        sum = get_sum(tg_id=callback_query.message.chat.id)
        keyboard.add(types.InlineKeyboardButton(text='Продлить подписку',url=sum))
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.send_message(
            callback_query.message.chat.id,
            text='Ваша подписка истекла. Хотите продлить подписку?',
            reply_markup=keyboard,
        )
        # Здесь можете отправить клавиатуру с кнопкой для покупки подписки
    else:
        text = f"<b>У вас активная подписка до</b> {subscription_end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        sum = get_sum(tg_id=callback_query.message.chat.id)
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='html'
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_ref')
async def check_ref(callback_query: types.CallbackQuery):
    text = 'Выберите способ'
    keyboard = types.InlineKeyboardMarkup()
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT who_linked FROM chats WHERE chat_id=?", (str(callback_query.message.chat.id), ))
    result = cursor.fetchone()
    if result[0]:
        keyboard.add(types.InlineKeyboardButton(text='🎯 Получить код', callback_data='get_code'))
        keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    else:
        keyboard.add(types.InlineKeyboardButton(text='🧩 Указать пригласительный код', callback_data='type_code'))
        keyboard.add(types.InlineKeyboardButton(text='🎯 Получить код', callback_data='get_code'))
        keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'get_code')
async def type_code(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.message.chat.id,f'Ваш пригласительный код <code>{callback_query.message.chat.id}</code>',parse_mode='html')

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'type_code')
async def type_code(callback_query: types.CallbackQuery,state: FSMContext):
    await SetCode.waiting_for_code.set()
    await bot.send_message(callback_query.message.chat.id,'Ввдеите пригласительный код')
    async with state.proxy() as data:
        data['chat_id'] = callback_query.message.chat.id

@dp.message_handler(state=SetCode.waiting_for_code)
async def enter_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        response_text = message.text

        # Проверяем, существует ли запись для данного chat_id и trigger
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chats WHERE chat_id=?", (str(chat_id), ))
        existing_record = cursor.fetchone()
        if existing_record:
            # Если запись существует, обновляем её
            cursor.execute("UPDATE chats SET who_linked=?  WHERE chat_id=?",
                           (response_text, str(chat_id)))


        conn.commit()
        conn.close()

        await message.reply(f"Пригласительный код записан")
        await state.finish()







@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_connection')
async def check_connection(callback_query: types.CallbackQuery):
    text = shablon_text
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_money')
async def check_money(callback_query: types.CallbackQuery):
    text = ''
    token = yoomoney_token
    client = Client(token)
    # Определите период времени, который считаете "последним месяцем"
    last_month_start = datetime.datetime.now() - datetime.timedelta(days=30)
    
    # Получаем список всех операций пользователя
    history = client.operation_history(label=callback_query.message.chat.id)
    

    
    # Добавляем заголовок текста с информацией о статусе платежа
    text += "<b>Статусы платежей за последний месяц:</b>\n\n"
    
    recent_operations = []
    
    for operation in history.operations:
        # Проверяем, что операция была успешной (статус "success") и находится в пределах последнего месяца
        if operation.status == "success" and operation.datetime >= last_month_start:
            recent_operations.append(operation)
    
    if recent_operations:
        for i, recent_operation in enumerate(recent_operations):
            print(f"Operation {i + 1}:", recent_operation.operation_id)
            print("\tStatus     -->", recent_operation.status)
            print("\tDatetime   -->", recent_operation.datetime)
            print("\tTitle      -->", recent_operation.title)
            print("\tPattern id -->", recent_operation.pattern_id)
            print("\tDirection  -->", recent_operation.direction)
            print("\tAmount     -->", recent_operation.amount)
            print("\tLabel      -->", recent_operation.label)
            print("\tType       -->", recent_operation.type)
            
            # Добавляем информацию о каждой успешной оплате к тексту сообщения
            text += f"<b>Платеж #{recent_operation.operation_id}</b>\n"
            text += f"Статус: {recent_operation.status}\n"
            text += f"Дата и время: {recent_operation.datetime}\n"
            text += f"Сумма: {recent_operation.amount}\n"
            text += f"Тип: {recent_operation.type}\n\n"
  
        how_much = len(recent_operations)
        subscription_end_date = get_subscription_end_date_from_database(callback_query.message.chat.id)
        if subscription_end_date is None or subscription_end_date < datetime.datetime.now():
        # Подписка истекла или отсутствует, добавьте месяц к текущей дате
            one_month_later = datetime.datetime.now() + datetime.timedelta(days=30*how_much)
            update_subscription_end_date_in_database(callback_query.message.chat.id, one_month_later)
        
  

        
    else:
        text += "У вас нет успешных оплат за последний месяц."
    
    # Создаем клавиатуру для возврата назад
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную
 
    # Отправляем сообщение с информацией о платеже и клавиатурой
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"  # Разрешаем использование HTML-разметки
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_chat_menu')
async def back_chat_menu(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='📋 Проверить статус подписки',callback_data='check_vip'))
    keyboard.add(types.InlineKeyboardButton(text='💳 Проверить платежи', callback_data='check_money'))
    keyboard.add(types.InlineKeyboardButton(text='➕ Подключить аккаунт',callback_data='check_connection'))
    keyboard.add(types.InlineKeyboardButton(text='🔌 Реф ссылка',callback_data='check_ref'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'video')
async def video_sos(callback_query: types.CallbackQuery):
    with open('full_video.mp4', 'rb') as video_file:
        # Send the video
            
        await bot.send_video(chat_id=callback_query.message.chat.id, video=video_file)


    # Introduce a delay using asyncio.sleep()
    await asyncio.sleep(2)  # Adjust the delay time as needed

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))
    
    
    # Используйте callback_query.message.chat.id и callback_query.message.message_id
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='https://youtu.be/HciXG9bnWRw',
        reply_markup=keyboard,
    )



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'test_period_start')
async def test_start(callback_query: types.CallbackQuery):
    user_id = callback_query.message.chat.id
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Проверяем, есть ли значение "тестовый период" для данного пользователя
    cursor.execute('SELECT test_period_end FROM clients WHERE id_telegram = ?', (user_id,))
    test_period_end = cursor.fetchone()

    if test_period_end is None:
        # Если значение "тестовый период" отсутствует, создаем новую запись
        test_period_end = datetime.datetime.now() + datetime.timedelta(days=7)
        cursor.execute('INSERT INTO clients (id_telegram, test_period_end) VALUES (?, ?)', (user_id, test_period_end))
    else:
        # Если значение "тестовый период" уже существует, обновляем его
        test_period_end = datetime.datetime.now() + datetime.timedelta(days=1)
        cursor.execute('UPDATE clients SET test_period_end = ? WHERE id_telegram = ?', (test_period_end, user_id))

    conn.commit()
    conn.close()

    # Отправляем сообщение о включении тестового периода
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться в главное меню',callback_data='back_main'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выдан тестовый доступ на 7 дней',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_wrapper')
async def back_wr(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='📹 Видео', callback_data='video'),
        types.InlineKeyboardButton(text='➕ Avito', callback_data='req_avito')
    )
    keyboard.add(
        types.InlineKeyboardButton(text='🕥 Тест', callback_data='test_period'),
        types.InlineKeyboardButton(text='📃 Отчеты', callback_data='auto_othcet')
    )
    keyboard.add(
        types.InlineKeyboardButton(text='🤖 Бот', callback_data='bot_connect'),
        types.InlineKeyboardButton(text='📤 Ответ', callback_data='bot_to_answer')
    )
    keyboard.add(
        types.InlineKeyboardButton(text='💾 Диалог', callback_data='bot_to_show'),
        types.InlineKeyboardButton(text='📑 Сценарии', callback_data='req_avito')
    )
    keyboard.add(types.InlineKeyboardButton(text='📚 Все чаты', callback_data='data_call'))
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться', callback_data='back_main'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    )



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'data_call')
async def test_period(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    media_group = []
    
    # Add each image to the media group
    media_group = []

    # Open the file outside the loop
    for filename in os.listdir(image_folder5):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file = open(os.path.join(image_folder5, filename), 'rb')
            media = types.InputMediaPhoto(file)
            media_group.append(media)

    text = data_text
    
    # Send the media group
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную
    await bot.send_media_group(callback_query.message.chat.id, media=media_group)
    
    # Send text and keyboard
    await bot.send_message(callback_query.message.chat.id, text=text, reply_markup=keyboard, parse_mode='html')



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'bot_connect')
async def test_period(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    # Отправляем изображения
    media_group = []

    # Open the file outside the loop
    for filename in os.listdir(image_folder2):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file = open(os.path.join(image_folder2, filename), 'rb')
            media = types.InputMediaPhoto(file)
            media_group.append(media)

    text = text_con
    
    # Отправляем текст и клавиатуру
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную
    await bot.send_media_group(callback_query.message.chat.id, media=media_group)

    await bot.send_message(callback_query.message.chat.id, text=text,reply_markup=keyboard,parse_mode='html')

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'bot_to_answer')
async def test_period(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))
    media_group = []

    # Open the file outside the loop
    for filename in os.listdir(image_folder3):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file = open(os.path.join(image_folder3, filename), 'rb')
            media = types.InputMediaPhoto(file)
            media_group.append(media)

    text = text_con

    # Send media group, text, and keyboard
    await bot.send_media_group(callback_query.message.chat.id, media=media_group)
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.send_message(callback_query.message.chat.id, text=text, reply_markup=keyboard, parse_mode='html')

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'bot_to_show')
async def test_period(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    # Отправляем изображения
    media_group = []

    # Open the file outside the loop
    for filename in os.listdir(image_folder4):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file = open(os.path.join(image_folder4, filename), 'rb')
            media = types.InputMediaPhoto(file)
            media_group.append(media)

    text = text_show
    
    # Отправляем текст и клавиатуру
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную
    await bot.send_media_group(callback_query.message.chat.id, media=media_group)

    await bot.send_message(callback_query.message.chat.id, text=text,reply_markup=keyboard,parse_mode='html')




@dp.callback_query_handler(lambda callback_query: callback_query.data == 'req_avito')
async def req_avito(callback_query: types.CallbackQuery):
    text = start_text
    text1 = instruct_first

    # Отправляем текст
    await bot.send_message(callback_query.message.chat.id, text=text, parse_mode='html')

    # Отправляем видео
    with open('video.gif', 'rb') as video_file:
        await bot.send_video(chat_id=callback_query.message.chat.id, video=video_file)

    # Отправляем второй текст
    await bot.send_message(callback_query.message.chat.id, text=text1, parse_mode='html')

    # Создаем кнопку "Вернуться назад"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    # Отправляем кнопку "Вернуться назад"
    await bot.send_message(callback_query.message.chat.id, text="Нажмите кнопку для возврата:", reply_markup=keyboard)

    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    # Если вы хотите, вы можете удалить предыдущее сообщение (например, текст "text" или видео) с помощью метода bot.delete_message().



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'auto_othcet')
async def auto_othcet(callback_query: types.CallbackQuery):
    text = work_auto_ans
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад',callback_data='back_wrapper'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='html'
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'test_period')
async def test_period(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    # Отправляем изображения
    media_group = []

    # Open the file outside the loop
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file = open(os.path.join(image_folder, filename), 'rb')
            media = types.InputMediaPhoto(file)
            media_group.append(media)

    text = test_periiod_text
    await bot.send_media_group(callback_query.message.chat.id, media=media_group)
    # Отправляем текст и клавиатуру
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.send_message(callback_query.message.chat.id, text=text,reply_markup=keyboard,parse_mode='html')

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'sos')
async def pomosh(callback_query: types.CallbackQuery):
    text = '''Выберите опцию'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='📃 Инструкция', callback_data='back_wrapper'),
        types.InlineKeyboardButton(text='📞 Поддержка', callback_data='sos_with_me')
    )
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_main'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'sos_with_me')
async def req_avito(callback_query: types.CallbackQuery):
    text = """
🤝 <b>Поддержка команды</b>
AvitoAuto готова помочь вам 24/7! Мы всегда рядом, чтобы предоставить качественную поддержку.

‼️ Отвечаем ежедневно с 10:00 до 00:00. Но не переживайте, мы также отвечаем в нерабочее время! Ваше удобство - наш приоритет.

📤 <a href="https://t.me/codenlx">Свяжитесь с нами</a> для получения быстрой и профессиональной помощи.

🚀 Мы готовы сделать все возможное, чтобы удовлетворить ваши потребности.

<i>С уважением, команда AvitoAuto</i>
"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад',callback_data='sos'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='html'
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'auto_answera')
async def auto_answera(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='🔍 Показать', callback_data='show_answers_table'),
        types.InlineKeyboardButton(text='➕ Добавить', callback_data='add_answer')
    )
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_main'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Подтвердите',
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_menu_show')
async def back_menu_show(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='🔍 Показать', callback_data='show_answers_table'),
        types.InlineKeyboardButton(text='➕ Добавить', callback_data='add_answer')
    )
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_main'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Подтвердите',
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'show_answers_table')
async def show_answers_table(callback_query: types.CallbackQuery):

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    user_id_telegram = callback_query.message.chat.id

    try:

        # Получаем user_id из таблицы clients
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Если нашли user_id, теперь получаем все чаты, привязанные к этому user_id
            cursor.execute('SELECT * FROM chats WHERE acc_id = ?', (user_id[0],))
            chats = cursor.fetchall()
            if chats:
                    # В переменной chats теперь хранятся все чаты, привязанные к заданному acc_id
                for chat in chats:
                    chat_id = chat[1]
                    id_avito = chat[2]
                    client_id = chat[3]
                    client_secret = chat[4]
                    token = chat[5]
                    test_period = chat[6]
                    token = get_token(chat_id)
                    profile = await get_profile(token=token)
                    profile_name = profile['name']
                    profile_url = profile['profile_url']
                    chat_info = await bot.get_chat(chat_id)
                    # Формируем текст сообщения
                    message_text = (
                        f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
                        f"<b>Название группы:</b> <code>{chat_info.title}</code>\n"
                        f"<b>Номер аккаунта:</b> <code>{user_id_telegram}</code>\n"
                        f"<b>Client_id:</b> <code>{client_id}</code>\n"
                        f"<b>Client_secret:</b> <code>{client_secret}</code>"
                    )

                    # Создаем кнопку "Выбрать"
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="Выбрать", callback_data=f"certainUser^{chat_id}"))
                    keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_menu_show'))

                    # Отправляем сообщение с разметкой и кнопкой
                    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

                    await bot.send_message(callback_query.message.chat.id, text=message_text, parse_mode="html", reply_markup=keyboard)
            else:
                # Если нет привязанных чатов, показываем диалоговое окно
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_menu_show'))

                await bot.answer_callback_query(callback_query.id, text='Вы не добавили аккаунт Авито.', show_alert=True)

        
    except:
        await bot.answer_callback_query(callback_query.id, text='Не подключен авито аккаунт в чате', show_alert=True)



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('certainUser^')))
async def certainUser(callback_query: types.CallbackQuery):
    action_data = callback_query.data.split('^')
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    chat_id = action_data[1]  # Получаем chat_id из action_data
    if chat_id:
        # Проверка таблицы 'msgs'
        cursor.execute('SELECT * FROM msgs WHERE chat_id = ?', (chat_id,))
        msgs_data = cursor.fetchone()

        # Проверка таблицы 'time_msgs'
        cursor.execute('SELECT * FROM time_msgs WHERE chat_id = ?', (chat_id,))
        time_msgs_data = cursor.fetchone()

        # Проверка таблицы 'auto_responses'
        cursor.execute('SELECT * FROM auto_responses WHERE chat_id = ?', (chat_id,))
        auto_responses_data = cursor.fetchone()

        # Создаем сообщение
        token = get_token(chat_id)
        profile = await get_profile(token=token)
        profile_name = profile['name']
        profile_url = profile['profile_url']
            # Формируем текст сообщения

        message_text = f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
        message_text2 = f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
        message_text3 = f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"

        # Добавляем информацию из таблиц 'msgs', 'time_msgs', 'auto_responses'
        if msgs_data:
            message_text+= f'Название: <b>Автоответ на первое сообщение</b>\n'
            message_text+= f'Заголовок: {msgs_data[1]}\n'
            message_text+= f'Дни недели: {msgs_data[4]}\n'
            message_text+= f'Вопрос: {msgs_data[-3]}\n'
            message_text+= f'Ответ: {msgs_data[-2]}\n'

            keyboard = types.InlineKeyboardMarkup()
            if msgs_data[3] == 1:
                keyboard.add(types.InlineKeyboardButton(text='Выкл',callback_data=f'autoOff_{chat_id}'))
            else:
                keyboard.add(types.InlineKeyboardButton(text='Вкл',callback_data=f'autoOn_{chat_id}'))

            keyboard.add(types.InlineKeyboardButton(text='Удалить',callback_data=f'autoDelete_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить название загаловка',callback_data=f'autoChzag_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить дни недель',callback_data=f'autoChangeDate_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить ответ',callback_data=f'autoChangeAns_{chat_id}'))
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            await bot.send_message(callback_query.message.chat.id,text=message_text,reply_markup=keyboard,parse_mode='html')
            
            # Добавляем информацию из таблицы 'msgs'

        if time_msgs_data:
            message_text2+= f'Название: <b>Сообщение в определенное время</b>\n'
            message_text2+= f'Заголовок: {time_msgs_data[1]}\n'
            message_text2+= f'Дни недели: {time_msgs_data[4]}\n'
            message_text2+= f'Ответ: {time_msgs_data[-3]}\n'
            message_text2+= f'Начало: {time_msgs_data[-2]}\n'
            message_text2+= f'Конец: {time_msgs_data[-1]}\n'

            keyboard = types.InlineKeyboardMarkup()
            if time_msgs_data[3] == 1:
                keyboard.add(types.InlineKeyboardButton(text='Выкл',callback_data=f'Timeoff_{chat_id}'))
            else:
                keyboard.add(types.InlineKeyboardButton(text='Вкл',callback_data=f'TimeOn_{chat_id}'))

            keyboard.add(types.InlineKeyboardButton(text='Удалить',callback_data=f'Timedelete_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить название загаловка',callback_data=f'TimeChangeZag_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить дни недель',callback_data=f'TimeChangeDate_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить ответ',callback_data=f'TimeChangeAns_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить время',callback_data=f'TimeChangeTime_{chat_id}'))
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            await bot.send_message(callback_query.message.chat.id,text=message_text2,reply_markup=keyboard,parse_mode='html')
            

        if auto_responses_data:
            message_text3+= f'Название: <b>Триггеры</b>\n'
            message_text3+= f'Заголовок: {auto_responses_data[-3]}\n'
            message_text3+= f'Ответ: {auto_responses_data[-1]}\n'


            keyboard = types.InlineKeyboardMarkup()
            if auto_responses_data[3] == 1:
                keyboard.add(types.InlineKeyboardButton(text='Выкл',callback_data=f'TrOff_{chat_id}'))
            else:
                keyboard.add(types.InlineKeyboardButton(text='Вкл',callback_data=f'TrOn_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Удалить',callback_data=f'TrDelete_{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text='Изменить триггеры',callback_data=f'TrCangeTriggers_{chat_id}'))

            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную
            await bot.send_message(callback_query.message.chat.id,text=message_text3,reply_markup=keyboard,parse_mode='html')
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную
            await bot.send_message(callback_query.message.chat.id,'У вас нет подготовленных сообщений)')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться в меню',callback_data='back_menu_show'))


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('Troff', 'TrOn','TrDelete','TrCangeTriggers','TrChangeAns')))
async def Trprocessing(callback_query: types.CallbackQuery,state: FSMContext):
    action = callback_query.data.split('_')
    await state.update_data(chat_id = action[1])
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    if action[0] == 'Troff':
        cursor.execute("UPDATE auto_responses SET enabled=?  WHERE chat_id=?",
                           (0,  str(action[1])))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Триггеры успешно выключены')
    elif action[0] == 'TrOn':
        cursor.execute("UPDATE auto_responses SET enabled=?  WHERE chat_id=?",
                           (1,  str(action[1])))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Триггеры успешно включены')
    elif action[0] == 'TrDelete':
        cursor.execute("DELETE FROM auto_responses WHERE chat_id=?",
                           (str(action[1]),))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Треггир успешно удален')
    elif action[0] == 'TrCangeTriggers':
        # Если это выбрано, переключитесь на ввод триггеров
        text = '''📝Введите триггеры, на которые нужно дать ответ. Триггером будет являться слово или словосочетание в сообщение клиента.

        Каждый триггер должен быть на новой строке и отправлены одним сообщением.

        Пример:
        Какая цена
        Цена какая
        Сколько стоит
        Узнать цену
        Узнать стоимость'''
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='stopp'))
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.send_message(callback_query.message.chat.id, text=text,reply_markup=keyboard)
        await ChangeAutoTriggers.WaitingForTrigger.set()
 




@dp.callback_query_handler(lambda callback_query: callback_query.data =='stopp', state=ChangeAutoTriggers)
async def stopp(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.message.chat.id,'Действие отменено')


@dp.message_handler(state=ChangeAutoTriggers.WaitingForTrigger)
async def enter_trigger(message: types.Message, state: FSMContext):
    # Ваш код для обработки триггера
    async with state.proxy() as data:
        chat_id = data['chat_id']
        trigger = message.text
        await state.update_data(trigger=trigger)

        await message.reply(f"Теперь введите ответ на триггер '{trigger}':")
        await AutoTriggers.WaitingForResponse.set()


@dp.message_handler(state=ChangeAutoTriggers.WaitingForResponse)
async def enter_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        trigger = data['trigger']
        response_text = message.text

        # Проверяем, существует ли запись для данного chat_id и trigger
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auto_responses WHERE chat_id=?", (str(chat_id), ))
        existing_record = cursor.fetchone()
        if existing_record:
            # Если запись существует, обновляем её
            cursor.execute("UPDATE auto_responses SET trigger=?, response_text=?  WHERE chat_id=?",
                           (trigger, response_text, str(chat_id)))
        else:
            # Если запись не существует, создаем новую
            cursor.execute("INSERT INTO auto_responses (chat_id, trigger, enabled response_text) VALUES (?, ?, ?)",
                           (str(chat_id), trigger, 1 ,response_text))

        conn.commit()
        conn.close()

        await message.reply(f"Триггер '{trigger}' и его ответ обновлены.")
        await state.finish()






@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('autoOff', 'autoOn', 'autoDelete','autoChzag','autoChangeDate','autoChangeAns')))
async def auto_processing(callback_query: types.CallbackQuery,state: FSMContext):
    action = callback_query.data.split('_')
    await state.update_data(chat_id = action[1])
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    if action[0] == 'autoOff':
        cursor.execute("UPDATE msgs SET enabled=?  WHERE chat_id=?",
                           (0,  str(action[1])))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Автоответ на приветсвтенное сообщение выключен')

    elif action[0] == 'autoOn':
        cursor.execute("UPDATE msgs SET enabled=?  WHERE chat_id=?",
                           (1,  str(action[1])))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Автоответ на приветсвтенное сообщение включен')
    elif action[0] == 'autoDelete':
        cursor.execute("DELETE FROM msgs WHERE chat_id=?",
                           (str(action[1]),))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Автоответ на приветсвтенное сообщение успешно удален')
    elif action[0] == 'autoChzag':
        await bot.send_message(callback_query.message.chat.id,'Введите новый загаловок')
        await ChangeAutoResponseStateTitle.waiting_for_title.set()
    elif action[0] == 'autoChangeDate':
        await ChangeAutoResponseStateWeekDaysChange.waiting_for_weekdays_change.set()
        markup = change_get_week_days_keyboard([])
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await callback_query.message.answer("Выберите дни недели, для которых будет активен автоответ:", reply_markup=markup)

    elif action[0] == 'autoChangeAns':
        await bot.send_message(callback_query.message.chat.id,'Введите новый ответ')
        await ChangeAutoResponseStateAnswer.waiting_for_answer.set()





@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('changeChoose_day_'), state=ChangeAutoResponseStateWeekDaysChange.waiting_for_weekdays_change)
async def choose_day(callback_query: types.CallbackQuery, state: FSMContext):
    selected_day = callback_query.data.split('_')[2]
    async with state.proxy() as data:
        chat_id = data['chat_id']  # Получаем chat_id из состояния

        if selected_day == "done":
            # Выход из состояния выбора дней недели
            await state.finish()
            await bot.send_message(callback_query.message.chat.id, "Настройки автоответа сохранены.")
            
            # Выполните здесь операцию вставки в базу данных
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            selected_days = data.get('selected_days', [])
            week_days_string = ",".join(selected_days)  # Строка, где дни недели разделены запятыми
            cursor.execute("UPDATE msgs SET week_days = ? WHERE chat_id = ?", (week_days_string, chat_id))

            conn.commit()
            conn.close()
            
        else:
            # Обработка выбора дня недели
            selected_days = data.get('selected_days', [])
            if selected_day == "all":
                selected_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
            elif selected_day in selected_days:
                selected_days.remove(selected_day)
            else:
                selected_days.append(selected_day)

            data['selected_days'] = selected_days
            updated_markup = change_get_updated_week_days_keyboard(selected_days)
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)
# Функция для создания клавиатуры выбора дней недели
def change_get_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "changeChoose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'changeChoose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="changeChoose_day_done"))
    return markup
# Функция для обновления клавиатуры выбора дней недели
def change_get_updated_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "changeChoose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'changeChoose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="changeChoose_day_done"))
    return markup
# Обработчик для кнопки "Выбрать все"
@dp.callback_query_handler(lambda callback_query: callback_query.data == "changeChoose_day_all", state=ChangeAutoResponseStateWeekDaysChange.waiting_for_weekdays_change)
async def changeChoose_day_all(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['selected_days'] = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        updated_markup = change_get_updated_week_days_keyboard(data['selected_days'])
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)




#------Change answer for msgs-----
@dp.message_handler(state=ChangeAutoResponseStateAnswer.waiting_for_answer)
async def enter_answer(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    async with state.proxy() as data:
        chat_id = data['chat_id']  # Получаем chat_id из состояния
        answer = message.text        
        cursor.execute("UPDATE msgs SET response_text=?  WHERE chat_id=?",
                            (answer,  chat_id))
        conn.commit()
        await bot.send_message(chat_id=message.chat.id,text='Ответ успешно изменен')
    await state.finish()  # Завершаем состояние после обработки сообщения

#change title for msgs
@dp.message_handler(state=ChangeAutoResponseStateTitle.waiting_for_title)
async def enter_title(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    async with state.proxy() as data:
        chat_id = data['chat_id']  # Получаем chat_id из состояния
        title = message.text        
        cursor.execute("UPDATE msgs SET title=?  WHERE chat_id=?",
                            (title,  chat_id))
        await bot.send_message(chat_id=message.chat.id,text='Загаловок успешно изменен')

        conn.commit()
    await state.finish()  # Завершаем состояние после обработки сообщения

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('Timeoff', 'TimeOn' ,'Timedelete','TimeChangeZag','TimeChangeDate','TimeChangeTime','TimeChangeAns')))
async def auto_processing(callback_query: types.CallbackQuery,state: FSMContext):
    action = callback_query.data.split('_')
    await state.update_data(chat_id = action[1])
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    if action[0] == 'Timeoff':
        cursor.execute("UPDATE time_msgs SET enabled=?  WHERE chat_id=?",
                           (0,  str(action[1])))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Автоответ на запланированное сообщение успешно выключен')
    elif action[0] == 'TimeOn':
        cursor.execute("UPDATE time_msgs SET enabled=?  WHERE chat_id=?",
                           (1,  str(action[1])))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Автоответ на запланированное сообщение успешно включен')
    
    elif action[0] == 'Timedelete':
        cursor.execute("DELETE FROM time_msgs WHERE chat_id=?",
                           (str(action[1]),))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id,'Автоответ на запланированное сообщение  успешно удален')
    elif action[0] == 'TimeChangeZag':
        await bot.send_message(callback_query.message.chat.id,'Введите новый загаловок')
        await TimeChangeAutoResponseStateTitle.waiting_for_title.set()
    elif action[0] == 'TimeChangeDate':
        await ChangeTimeResponseStateWeekDays.waiting_for_weekdays.set()
        markup = time_change_get_week_days_keyboard([])
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await callback_query.message.answer("Выберите дни недели, для которых будет активен автоответ:", reply_markup=markup)

    elif action[0] == 'TimeChangeAns':
        await bot.send_message(callback_query.message.chat.id,'Введите новый ответ')
        await TimeChangeAutoResponseStateAnswer.waiting_for_answer.set()
    elif action[0] == 'TimeChangeTime':
        await bot.send_message(callback_query.message.chat.id,'Введите новое время по примеру (00:00)')
        await ChangeTimeResponseStateStartTime.waiting_for_start_time.set()




#----------Change Date Time---------


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('TimechangeChoose_day_'), state=ChangeTimeResponseStateWeekDays.waiting_for_weekdays)
async def time_choose_day(callback_query: types.CallbackQuery, state: FSMContext):
    selected_day = callback_query.data.split('_')[2]
    async with state.proxy() as data:
        chat_id = data['chat_id']  # Получаем chat_id из состояния

        if selected_day == "done":
            # Выход из состояния выбора дней недели
            await state.finish()
            await bot.send_message(callback_query.message.chat.id, "Настройки автоответа сохранены.")
            
            # Выполните здесь операцию вставки в базу данных
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            selected_days = data.get('selected_days', [])
            week_days_string = ",".join(selected_days)  # Строка, где дни недели разделены запятыми
            cursor.execute("UPDATE time_msgs SET week_days = ? WHERE chat_id = ?", (week_days_string, chat_id))

            conn.commit()
            conn.close()
            
        else:
            # Обработка выбора дня недели
            selected_days = data.get('selected_days', [])
            if selected_day == "all":
                selected_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
            elif selected_day in selected_days:
                selected_days.remove(selected_day)
            else:
                selected_days.append(selected_day)

            data['selected_days'] = selected_days
            updated_markup = time_change_get_updated_week_days_keyboard(selected_days)
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)
# Функция для создания клавиатуры выбора дней недели
def time_change_get_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "TimechangeChoose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'TimechangeChoose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="TimechangeChoose_day_done"))
    return markup
# Функция для обновления клавиатуры выбора дней недели
def time_change_get_updated_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "TimechangeChoose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'TimechangeChoose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="TimechangeChoose_day_done"))
    return markup
# Обработчик для кнопки "Выбрать все"
@dp.callback_query_handler(lambda callback_query: callback_query.data == "TimechangeChoose_day_all", state=ChangeTimeResponseStateWeekDays.waiting_for_weekdays)
async def changeChoose_day_all(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['selected_days'] = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        updated_markup = time_change_get_updated_week_days_keyboard(data['selected_days'])
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)







@dp.message_handler(state=TimeChangeAutoResponseStateAnswer.waiting_for_answer)
async def enter_answer(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    async with state.proxy() as data:
        chat_id = data['chat_id']  # Получаем chat_id из состояния
        answer = message.text        
        cursor.execute("UPDATE time_msgs SET response_text=?  WHERE chat_id=?",
                            (answer,  chat_id))
        conn.commit()
        await bot.send_message(chat_id=message.chat.id,text='Ответ успешно изменен')
    await state.finish()  # Завершаем состояние после обработки сообщения

#change title for msgs
@dp.message_handler(state=TimeChangeAutoResponseStateTitle.waiting_for_title)
async def enter_title(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    async with state.proxy() as data:
        chat_id = data['chat_id']  # Получаем chat_id из состояния
        title = message.text        
        cursor.execute("UPDATE time_msgs SET title=?  WHERE chat_id=?",
                            (title,  chat_id))
        await bot.send_message(chat_id=message.chat.id,text='Загаловок успешно изменен')

        conn.commit()
    await state.finish()  # Завершаем состояние после обработки сообщения







@dp.message_handler(lambda message: not message.text.startswith('/'), state=ChangeTimeResponseStateStartTime.waiting_for_start_time)
async def time_change_process_start_time_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            time_str = message.text.strip()
            # Парсим введенное время
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours < 24) or not (0 <= minutes < 60):
                raise ValueError
            # Преобразуем введенное время в строку формата HH:MM
            time_formatted = f"{hours:02d}:{minutes:02d}"
            data['start_time'] = time_formatted
        except ValueError:
            await message.answer("Пожалуйста, введите корректное время начала интервала в формате HH:MM.")
            return

    await ChangeTimeResponseStateEndTime.waiting_for_end_time.set()
    await message.answer("Теперь введите время окончания интервала в формате HH:MM.")

@dp.message_handler(lambda message: not message.text.startswith('/'), state=ChangeTimeResponseStateEndTime.waiting_for_end_time)
async def time_change_process_end_time_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            time_str = message.text.strip()
            # Парсим введенное время
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours < 24) or not (0 <= minutes < 60):
                raise ValueError
            # Преобразуем введенное время в строку формата HH:MM
            time_formatted = f"{hours:02d}:{minutes:02d}"
            data['end_time'] = time_formatted
        except ValueError:
            await message.answer("Пожалуйста, введите корректное время окончания интервала в формате HH:MM.")
            return

    await message.answer("Ввод времени завершен.")
    await time_change_process_time_interval_data(message, state)

async def time_change_process_time_interval_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        chat_id = data['chat_id']
        start_time = data['start_time']
        end_time = data['end_time']

        cursor.execute("UPDATE time_msgs SET start_time=?, end_time=? WHERE chat_id=?", (start_time, end_time, chat_id))

        conn.commit()
        conn.close()

        await message.answer(f"Интервал времени успешно изменен: с {start_time} до {end_time}")

        # Возвращаемся в начальное состояние
        await state.finish()





#------------Меняем дату-------------





@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_answer')
async def add_answer(callback_query: types.CallbackQuery):
    text = '''Выберите, в каком случае будем отправлять сообщение клиенту ⁉️ Будьте внимательны, автоответы будут применены для всех аккаунтов привязанных к боту. Если у вас несколько аккаунтов и вы вы хотите, чтобы в каждом аккаунте была своя логика. Создайте для каждого аккаунта отдельный чат в Telegram и добавьте туда бота для работы с сообщениями.'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='1-е сообщение', callback_data='first_message'),
        types.InlineKeyboardButton(text='🔔 Триггеры', callback_data='triggers')
    )
    keyboard.add(types.InlineKeyboardButton(text='⏰ Промежуток времени', callback_data='time_message')
)
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_menu_show'))
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    ) 


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'time_message')
async def time_message(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    user_id_telegram = callback_query.message.chat.id

    try:

        # Получаем user_id из таблицы clients
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Если нашли user_id, теперь получаем все чаты, привязанные к этому user_id
            cursor.execute('SELECT * FROM chats WHERE acc_id = ?', (user_id[0],))
            chats = cursor.fetchall()
            if chats:
                # В переменной chats теперь хранятся все чаты, привязанные к заданному acc_id
                for chat in chats:
                    chat_id = chat[1]
                    id_avito = chat[2]
                    client_id = chat[3]
                    client_secret = chat[4]
                    token = chat[5]
                    test_period = chat[6]
                    token = get_token(chat_id)
                    profile = await get_profile(token=token)
                    profile_name = profile['name']
                    profile_url = profile['profile_url']
                    chat_info = await bot.get_chat(chat_id)
                    # Формируем текст сообщения
                    message_text = (
                        f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
                        f"<b>Название группы:</b> <code>{chat_info.title}</code>\n"
                        f"<b>Номер аккаунта:</b> <code>{user_id_telegram}</code>\n"
                        f"<b>Client_id:</b> <code>{client_id}</code>\n"
                        f"<b>Client_secret:</b> <code>{client_secret}</code>"
                    )

                    # Создаем кнопку "Выбрать"
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="Выбрать", callback_data=f"time_select^{chat_id}"))

                    # Отправляем сообщение с разметкой и кнопкой
                    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

                    await bot.send_message(callback_query.message.chat.id, text=message_text, parse_mode="html", reply_markup=keyboard)

                    # Дальше можно делать что-то с данными о чатах
            else:
                # Если нет привязанных чатов, показываем диалоговое окно
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_menu_show'))

                await bot.answer_callback_query(callback_query.id, text='Вы не добавили аккаунт Авито.', show_alert=True)

    except:
        await bot.send_message(callback_query.message.chat.id,'haha')

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('cancel')))
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.message.chat.id,'Обработка отменена')
    
# Обработчик для начала установки настроек автоответа
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('time_select^')))
async def select_callback(callback_query: types.CallbackQuery, state: FSMContext):
    action_data = callback_query.data.split('^')
    chat_id = action_data[1]  # Получаем chat_id из action_data
    await state.update_data(chat_id=chat_id)  # Сохраняем chat_id в состоянии FSM
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Отменить',callback_data='cancel'))
    await TimeResponseStateTitle.waiting_for_title.set()
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await callback_query.message.reply("Введите заголовок автоответа:")
    await bot.send_message(callback_query.message.chat.id,'Можете отменить',reply_markup=keyboard)

# Обработчик для ввода заголовка


# Обработчик для ввода ids объявления
@dp.message_handler(state=TimeResponseStateTitle.waiting_for_title)
async def enter_avito_ids(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await TimeResponseStateText.waiting_for_text.set()
    await message.answer("Введите текст сообщения:")

# Обработчик для ввода текста сообщения
@dp.message_handler(state=TimeResponseStateText.waiting_for_text)
async def enter_response_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['response_text'] = message.text
    await TimeResponseStateWeekDays.waiting_for_weekdays.set()
    markup = work_get_week_days_keyboard([])

    await message.answer("Выберите дни недели, для которых будет активен автоответ:", reply_markup=markup)

#----------------Обработчик недели на сообщение в опред время-----------------

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('work_choose_day_'), state=TimeResponseStateWeekDays.waiting_for_weekdays)
async def work_choose_day(callback_query: types.CallbackQuery, state: FSMContext):
    selected_day = callback_query.data.split('_')[3]
    async with state.proxy() as data:
        chat_id = callback_query.message.chat.id
        chat_id_from_state = data.get('chat_id', chat_id)
        title = data.get('title')
        response_text = data.get('response_text')

        if selected_day == "done":
            # Выход из состояния выбора дней недели
            await state.update_data(selected_days=data.get('selected_days', []))
            await TimeResponseStateStartTime.waiting_for_start_time.set()
            await bot.send_message(callback_query.message.chat.id, "Введите время начала интервала в формате HH:MM. (08:00)")
            
        else:
            # Обработка выбора дня недели
            selected_days = data.get('selected_days', [])
            if selected_day == "all":
                selected_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
            elif selected_day in selected_days:
                selected_days.remove(selected_day)
            else:
                selected_days.append(selected_day)

            data['selected_days'] = selected_days
            updated_markup = work_get_updated_week_days_keyboard(selected_days)
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)
            

@dp.message_handler(lambda message: not message.text.startswith('/'), state=TimeResponseStateStartTime.waiting_for_start_time)
async def process_start_time_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            time_str = message.text.strip()
            # Парсим введенное время
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours < 24) or not (0 <= minutes < 60):
                raise ValueError
            # Преобразуем введенное время в строку формата HH:MM
            time_formatted = f"{hours:02d}:{minutes:02d}"
            data['start_time'] = time_formatted
        except ValueError:
            await message.answer("Пожалуйста, введите корректное время начала интервала в формате HH:MM.")
            return

    await TimeResponseStateEndTime.waiting_for_end_time.set()
    await message.answer("Теперь введите время окончания интервала в формате HH:MM.")

@dp.message_handler(lambda message: not message.text.startswith('/'), state=TimeResponseStateEndTime.waiting_for_end_time)
async def process_end_time_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            time_str = message.text.strip()
            # Парсим введенное время
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours < 24) or not (0 <= minutes < 60):
                raise ValueError
            # Преобразуем введенное время в строку формата HH:MM
            time_formatted = f"{hours:02d}:{minutes:02d}"
            data['end_time'] = time_formatted
        except ValueError:
            await message.answer("Пожалуйста, введите корректное время окончания интервала в формате HH:MM.")
            return

    await message.answer("Ввод времени завершен.")
    await process_time_interval_data(message, state)

async def process_time_interval_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        title = data['title']
        chat_id = data['chat_id']
        response_text = data['response_text']
        selected_days = data['selected_days']
        start_time = data['start_time']
        end_time = data['end_time']
        week_days_string = ",".join(selected_days)

        cursor.execute("INSERT OR REPLACE INTO time_msgs (title, chat_id, enabled, week_days,  response_text, start_time, end_time) VALUES (?, ?, ?,  ?, ?, ?, ?)",
                       (title, chat_id, 1, week_days_string, response_text, start_time, end_time))
        conn.commit()
        conn.close()

        await message.answer(f"Настройки автоответа сохранены. Выбранные дни недели: {week_days_string}, Интервал времени: с {start_time} до {end_time}")

        # Возвращаемся в начальное состояние
        await state.finish()


# Функция для создания клавиатуры выбора дней недели
def work_get_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "work_choose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'work_choose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="work_choose_day_done"))
    return markup
# Функция для обновления клавиатуры выбора дней недели
def work_get_updated_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "work_choose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'work_choose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="work_choose_day_done"))
    return markup
# Обработчик для кнопки "Выбрать все"
@dp.callback_query_handler(lambda callback_query: callback_query.data == "work_choose_day_all", state=TimeResponseStateWeekDays.waiting_for_weekdays)
async def work_choose_day_al(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['selected_days'] = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        updated_markup = work_get_updated_week_days_keyboard(data['selected_days'])
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'triggers')
async def triggers(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    user_id_telegram = callback_query.message.chat.id

    try:

        # Получаем user_id из таблицы clients
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Если нашли user_id, теперь получаем все чаты, привязанные к этому user_id
            cursor.execute('SELECT * FROM chats WHERE acc_id = ?', (user_id[0],))
            chats = cursor.fetchall()
            if chats:
                # В переменной chats теперь хранятся все чаты, привязанные к заданному acc_id
                for chat in chats:
                    chat_id = chat[1]
                    id_avito = chat[2]
                    client_id = chat[3]
                    client_secret = chat[4]
                    token = chat[5]
                    test_period = chat[6]
                    token = get_token(chat_id)
                    profile = await get_profile(token=token)
                    profile_name = profile['name']
                    profile_url = profile['profile_url']
                    chat_info = await bot.get_chat(chat_id)
                    # Формируем текст сообщения
                    message_text = (
                        f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
                        f"<b>Название группы:</b> <code>{chat_info.title}</code>\n"
                        f"<b>Номер аккаунта:</b> <code>{user_id_telegram}</code>\n"
                        f"<b>Client_id:</b> <code>{client_id}</code>\n"
                        f"<b>Client_secret:</b> <code>{client_secret}</code>"
                    )

                    # Создаем кнопку "Выбрать"
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="Выбрать", callback_data=f"trig^{chat_id}"))

                    # Отправляем сообщение с разметкой и кнопкой
                    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

                    await bot.send_message(callback_query.message.chat.id, text=message_text, parse_mode="html", reply_markup=keyboard)

                    # Дальше можно делать что-то с данными о чатах
            else:
                # Если нет привязанных чатов, показываем диалоговое окно
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_menu_show'))

                await bot.answer_callback_query(callback_query.id, text='Вы не добавили аккаунт Авито.', show_alert=True)

    except:
        await bot.answer_callback_query(callback_query.id, text='Не подключен авито аккаунт в чате', show_alert=True)




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('trig^')))
async def select_callback(callback_query: types.CallbackQuery, state: FSMContext):
    action_data = callback_query.data.split('^')
    chat_id = action_data[1]  # Получаем chat_id из action_data

    text = '''📝Введите триггеры, на которые нужно дать ответ. Триггером будет являться слово или словосочетание в сообщение клиента.

    Каждый триггер должен быть на новой строке и отправлены одним сообщением.

    Пример:
    Какая цена
    Цена какая
    Сколько стоит
    Узнать цену
    Узнать стоимость'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='stopp'))

    await bot.send_message(callback_query.message.chat.id, text=text,reply_markup=keyboard)
    await state.update_data(chat_id=chat_id)  # Сохраняем chat_id в состоянии FSM
    await AutoTriggers.WaitingForTrigger.set()
    async with state.proxy() as data:
        data['chat_id'] = chat_id

    await callback_query.message.reply("Введите Триггеры:")

@dp.callback_query_handler(lambda callback_query: callback_query.data =='stopp', state=AutoTriggers)
async def stopp(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.message.chat.id,'Действие отменено')


@dp.message_handler(state=AutoTriggers.WaitingForTrigger)
async def enter_trigger(message: types.Message, state: FSMContext):
    # Ваш код для обработки триггера
    async with state.proxy() as data:
        chat_id = data['chat_id']
        trigger = message.text
        await state.update_data(trigger=trigger)
        await message.reply(f"Теперь введите ответ на триггер '{trigger}':")
        await AutoTriggers.WaitingForResponse.set()


@dp.message_handler(state=AutoTriggers.WaitingForResponse)
async def enter_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        trigger = data['trigger']
        response_text = message.text

        # Проверяем, существует ли запись для данного chat_id и trigger
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auto_responses WHERE chat_id=?", (str(chat_id), ))
        existing_record = cursor.fetchone()
        if existing_record:
            # Если запись существует, обновляем её
            cursor.execute("UPDATE auto_responses SET trigger=?, response_text=?  WHERE chat_id=?",
                           (trigger, response_text, str(chat_id)))
        else:
            # Если запись не существует, создаем новую
            cursor.execute("INSERT INTO auto_responses (chat_id, trigger, enabled, response_text) VALUES (?, ?, ?, ?)",
                           (str(chat_id), trigger, 1 ,response_text))

        conn.commit()
        conn.close()

        await message.reply(f"Триггер '{trigger}' и его ответ обновлены.")
        await state.finish()




#На первое сообщение функция 

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'first_message')
async def first_message(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    user_id_telegram = callback_query.message.chat.id

    try:

        # Получаем user_id из таблицы clients
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Если нашли user_id, теперь получаем все чаты, привязанные к этому user_id
            cursor.execute('SELECT * FROM chats WHERE acc_id = ?', (user_id[0],))
            chats = cursor.fetchall()
            if chats:
                # В переменной chats теперь хранятся все чаты, привязанные к заданному acc_id
                for chat in chats:
                    chat_id = chat[1]
                    id_avito = chat[2]
                    client_id = chat[3]
                    client_secret = chat[4]
                    token = chat[5]
                    test_period = chat[6]
                    token = get_token(chat_id)
                    profile = await get_profile(token=token)
                    profile_name = profile['name']
                    profile_url = profile['profile_url']
                    chat_info = await bot.get_chat(chat_id)
                    # Формируем текст сообщения
                    message_text = (
                        f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
                        f"<b>Название группы:</b> <code>{chat_info.title}</code>\n"
                        f"<b>Номер аккаунта:</b> <code>{user_id_telegram}</code>\n"
                        f"<b>Client_id:</b> <code>{client_id}</code>\n"
                        f"<b>Client_secret:</b> <code>{client_secret}</code>"
                    )

                    # Создаем кнопку "Выбрать"
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="Выбрать", callback_data=f"select^{chat_id}"))

                    # Отправляем сообщение с разметкой и кнопкой
                    await bot.send_message(callback_query.message.chat.id, text=message_text, parse_mode="html", reply_markup=keyboard)

                    # Дальше можно делать что-то с данными о чатах
            else:
                # Если нет привязанных чатов, показываем диалоговое окно
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='back_menu_show'))

                await bot.answer_callback_query(callback_query.id, text='Вы не добавили аккаунт Авито.', show_alert=True)

    except:
        await bot.answer_callback_query(callback_query.id, text='Вы не добавили аккаунт Авито.', show_alert=True)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_main')
async def back_main(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    print(callback_query.message.chat.id)
    if callback_query.message.chat.id in admin_ids:
        keyboard.add(
            types.InlineKeyboardButton(text='🎥 Видео', callback_data='video'),
            types.InlineKeyboardButton(text='📋 Список аккаунтов', callback_data='spisok')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='🤖 Автоответы', callback_data='auto_answera'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='sos')
    )
        keyboard.add(types.InlineKeyboardButton(text='Админ панель',callback_data='acc_back'))
    else:
        keyboard.add(
            types.InlineKeyboardButton(text='🎥 Видео', callback_data='video'),
            types.InlineKeyboardButton(text='📋 Список аккаунтов', callback_data='spisok')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='🤖 Автоответы', callback_data='auto_answera'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='sos')
    )
    try:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        # Проверяем, есть ли значение в атрибуте "тестовый период" для данного пользователя
        cursor.execute('SELECT test_period_end FROM clients WHERE id_telegram = ?', (callback_query.message.chat.id,))
        test_period_end = cursor.fetchone()
        conn.close()
        
        if test_period_end[0] is None:
            # Если значение "тестовый период" отсутствует, добавляем кнопку "тестовый период" в клавиатуру
            keyboard.add(types.InlineKeyboardButton(text='🕒 Тестовый период', callback_data='test_period_start'))
    except:
        pass
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    ) 

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'spisok')
async def spisok(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    user_id_telegram = callback_query.message.chat.id

    try:

        # Получаем user_id из таблицы clients
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Если нашли user_id, теперь получаем все чаты, привязанные к этому user_id
            cursor.execute('SELECT * FROM chats WHERE acc_id = ?', (user_id[0],))
            chats = cursor.fetchall()
            if chats:

                    # В переменной chats теперь хранятся все чаты, привязанные к заданному acc_id
                for chat in chats:
                    chat_id = chat[1]
                    id_avito = chat[2]
                    client_id = chat[3]
                    client_secret = chat[4]
                    token = chat[5]
                    test_period = chat[6]
                    token = get_token(chat_id)
                    profile = await get_profile(token=token)
                    profile_name = profile['name']
                    profile_url = profile['profile_url']
                    chat_info = await bot.get_chat(chat_id)
                    # Формируем текст сообщения
                    message_text = (
                        f"<b>Профиль:</b> <a href='{profile_url}'>{profile_name}</a>\n"
                        f"<b>Название группы:</b> <code>{chat_info.title}</code>\n"
                        f"<b>Номер аккаунта:</b> <code>{user_id_telegram}</code>\n"
                        f"<b>Client_id:</b> <code>{client_id}</code>\n"
                        f"<b>Client_secret:</b> <code>{client_secret}</code>"
                    )

                    # Создаем кнопку "Выбрать"
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться в главное меню',callback_data='back_main'))
                    # Отправляем сообщение с разметкой и кнопкой
                    await bot.send_message(callback_query.message.chat.id, text=message_text, parse_mode="html", reply_markup=keyboard)



                # Дальше можно делать что-то с данными о чатах
        await bot.send_message(callback_query.message.chat.id,'Назад',reply_markup=keyboard)
    except:
        await bot.answer_callback_query(callback_query.id, text='Не подключен авито аккаунт в чате', show_alert=True)







#Состояния для ввода первого сообщения


# Обработчик для выбора дней недели
# Обработчик для выбора дней недели
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('choose_day_'), state=AutoResponseStateWeekDays.waiting_for_weekdays)
async def choose_day(callback_query: types.CallbackQuery, state: FSMContext):
    selected_day = callback_query.data.split('_')[2]
    async with state.proxy() as data:
        chat_id = callback_query.message.chat.id
        chat_id_from_state = data.get('chat_id', chat_id)
        title = data.get('title')
        response_text = data.get('response_text')

        if selected_day == "done":
            # Выход из состояния выбора дней недели
            await state.finish()
            await bot.send_message(callback_query.message.chat.id, "Настройки автоответа сохранены.")
            
            # Выполните здесь операцию вставки в базу данных
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            selected_days = data.get('selected_days', [])
            week_days_string = ",".join(selected_days)  # Строка, где дни недели разделены запятыми
            cursor.execute("INSERT OR REPLACE INTO msgs (title, chat_id, enabled, week_days,  response_text) VALUES (?, ?, ?, ?, ?)",
                           (title, chat_id_from_state, 1, week_days_string,  response_text))
            conn.commit()
            conn.close()
            
        else:
            # Обработка выбора дня недели
            selected_days = data.get('selected_days', [])
            if selected_day == "all":
                selected_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
            elif selected_day in selected_days:
                selected_days.remove(selected_day)
            else:
                selected_days.append(selected_day)

            data['selected_days'] = selected_days
            updated_markup = get_updated_week_days_keyboard(selected_days)
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)
# Функция для создания клавиатуры выбора дней недели
def get_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "choose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'choose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="choose_day_done"))
    return markup
# Функция для обновления клавиатуры выбора дней недели
def get_updated_week_days_keyboard(selected_days):
    markup = types.InlineKeyboardMarkup(row_width=4)  # Устанавливаем row_width на 4, чтобы было по два дня недели в строке
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    # Добавляем кнопку "Выбрать все"
    select_all_callback_data = "choose_day_all"
    select_all_text = "Выбрать все ✅" if all(day in selected_days for day in days) else "Выбрать все ❌"
    markup.add(types.InlineKeyboardButton(text=select_all_text, callback_data=select_all_callback_data))

    # Разбиваем дни недели на две строки
    for i in range(0, len(days), 4):
        row = days[i:i + 4]
        row_buttons = [
            types.InlineKeyboardButton(
                text=f'✅ {day}' if day in selected_days else f'❌ {day}',
                callback_data=f'choose_day_{day}'
            ) for day in row
        ]
        markup.row(*row_buttons)

    # Добавляем кнопку "Готово"
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="choose_day_done"))
    return markup
# Обработчик для кнопки "Выбрать все"
@dp.callback_query_handler(lambda callback_query: callback_query.data == "choose_day_all", state=AutoResponseStateWeekDays.waiting_for_weekdays)
async def choose_day_all(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['selected_days'] = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        updated_markup = get_updated_week_days_keyboard(data['selected_days'])
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_markup)


# Обработчик для начала установки настроек автоответа
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('select^')))
async def select_callback(callback_query: types.CallbackQuery, state: FSMContext):
    action_data = callback_query.data.split('^')
    chat_id = action_data[1]  # Получаем chat_id из action_data
    await state.update_data(chat_id=chat_id)  # Сохраняем chat_id в состоянии FSM
    await AutoResponseStateTitle.waiting_for_title.set()
    await callback_query.message.reply("Введите заголовок автоответа:")



# Обработчик для ввода ids объявления
@dp.message_handler(state=AutoResponseStateTitle.waiting_for_title)
async def enter_avito_ids(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await AutoResponseStateText.waiting_for_text.set()
    await message.answer("Введите текст сообщения:")

# Обработчик для ввода текста сообщения
@dp.message_handler(state=AutoResponseStateText.waiting_for_text)
async def enter_response_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['response_text'] = message.text
    await AutoResponseStateWeekDays.waiting_for_weekdays.set()
    markup = get_week_days_keyboard([])
    await message.answer("Выберите дни недели, для которых будет активен автоответ:", reply_markup=markup)




@dp.message_handler(Command("data") & ChatTypeFilter(types.ChatType.GROUP))
async def get_data(message: types.Message, just = None):
    current_page = 0
    current_page_message_id = None  # Инициализация переменной
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    message_id = message.message_id
    chat_id = message.chat.id  # Используйте актуальное значение chat_id

    cursor.execute("SELECT test_period FROM chats WHERE chat_id = ?", (chat_id,))
    test_period_str = cursor.fetchone()

    # Запрос текущей страницы и ID последнего сообщения для данного чата
    cursor.execute("SELECT current_page, current_page_message_id FROM chats WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    # Если есть результат, извлеките текущую страницу и ID сообщения
    if result[0] and result[1]:
        current_page, current_page_message_id = result[0],result[1]
    else:
        # Если нет результатов, установите начальные значения
        current_page = 0
        current_page_message_id = None

    # Define the number of contacts to display per page
    contacts_per_page = 6
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    # Clear the unique_user_names set for the current page
    unique_user_names.clear()
    user_id = get_user_id(message.chat.id)
    token = get_token(message.chat.id)

    avito_data = await get_avito_data(token=token,user_id=user_id)

    if test_period_str:
        test_period_str = test_period_str[0]
        test_period_str = test_period_str.split('.')[0]  # Remove the fractional seconds
        test_period = datetime.datetime.strptime(test_period_str, '%Y-%m-%d %H:%M:%S')

        if test_period > datetime.datetime.now():
            # Define the number of contacts to display per page

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
                    button = types.InlineKeyboardButton(text=name, callback_data=f'send^{cleaned_user_name}^{user_id}^{chat_id}')
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
                if message.text == '/data':
                    message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
                    current_page_message_id = message.message_id
                    cursor.execute("UPDATE chats SET current_page_message_id = ? WHERE chat_id = ?", (current_page_message_id, message.chat.id))
                    conn.commit()
                elif current_page_message_id and just==None:

                    try:
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=current_page_message_id,
                                                    text="Выберите пользователя:", reply_markup=keyboard)
                    except aiogram.utils.exceptions.MessageNotModified:
                        # Если сообщение не было изменено, просто пропустите ошибку
                            # Если сообщение не было изменено, удаляем предыдущее сообщение и отправляем новое
                        await bot.delete_message(chat_id=message.chat.id, message_id=current_page_message_id)
                        message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
                        current_page_message_id = message.message_id
                        cursor.execute("UPDATE chats SET current_page_message_id = ? WHERE chat_id = ?", (current_page_message_id, chat_id))
                        conn.commit()
                elif current_page_message_id and just=='response':
                        try:
                            await bot.send_message(chat_id=message.chat.id, message_id=current_page_message_id,
                                                        text="Выберите пользователя:", reply_markup=keyboard)
                            
                        except aiogram.utils.exceptions.MessageNotModified:
                            # Если сообщение не было изменено, просто пропустите ошибку
                                # Если сообщение не было изменено, удаляем предыдущее сообщение и отправляем новое
                            await bot.delete_message(chat_id=message.chat.id, message_id=current_page_message_id)
                            message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
                            current_page_message_id = message.message_id
                            cursor.execute("UPDATE chats SET current_page_message_id = ? WHERE chat_id = ?", (current_page_message_id, chat_id))
                            conn.commit()
            
                else:
                    # Send the initial message with the contacts and navigation buttons
                    message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
                    current_page_message_id = message.message_id
                    cursor.execute("UPDATE chats SET current_page_message_id = ? WHERE chat_id = ?", (current_page_message_id, message.chat.id))
                    conn.commit()

        else:
            await message.answer("Ваш тестовый период истек. Для продолжения работы, пожалуйста оплатите подписку")

    else:
        await message.answer("Произошла ошибка при получении данных из Avito.")

    conn.close()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('page_'))
async def page_navigation_callback(callback_query: types.CallbackQuery):
    page_number = int(callback_query.data.split('_')[1])
    
    # Получите chat_id из callback_query
    chat_id = callback_query.message.chat.id
    
    # Подключение к базе данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Извлеките актуальные данные из таблицы chats для данного чата
    cursor.execute("SELECT current_page, current_page_message_id FROM chats WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    
    # Если есть результат, извлеките текущую страницу и ID сообщения
    if result:
        current_page, current_page_message_id = result
    else:
        # Если нет результатов, установите начальные значения
        current_page = 0
        current_page_message_id = None

    # Обновите данные в таблице chats для данного чата
    cursor.execute("UPDATE chats SET current_page = ?, current_page_message_id = ? WHERE chat_id = ?", (page_number, current_page_message_id, chat_id))
    conn.commit()

    # Закрытие соединения
    conn.close()

    # Теперь можно обновить данные в функции get_data с использованием chat_id, current_page и current_page_message_id
    await get_data(callback_query.message)




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send^'))
async def process_callback(callback_query: types.CallbackQuery):
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
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную


    # Отправьте сообщение с клавиатурой
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите действие:',
        reply_markup=keyboard
    )

    
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('seend^'))
async def process_callback2(callback_query: types.CallbackQuery):
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
    chat_text = ''
    action_data = callback_query.data.split('^')
    action = action_data[0]
    print(action_data)
    if len(action_data)>2:
        user_id, chat_id  = action_data[1], action_data[2]
    else:
        pass

    if action == 'back':
        current_page = 0
        current_page_message_id = None
        callback_query.data = f'page_{current_page}'
        page_number = int(callback_query.data.split('_')[1])        
        # Получите chat_id из callback_query
        chat_id = callback_query.message.chat.id

        # Подключение к базе данных
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Извлеките актуальные данные из таблицы chats для данного чата
        cursor.execute("SELECT current_page, current_page_message_id FROM chats WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()
        
        # Если есть результат, извлеките текущую страницу и ID сообщения
        if result[0] and result[1]:
            current_page, current_page_message_id = result[0],result[1]
        else:
            # Если нет результатов, установите начальные значения
            current_page = 0
            current_page_message_id = None

        # Обновите данные в таблице chats для данного чата
        cursor.execute("UPDATE chats SET current_page = ?, current_page_message_id = ? WHERE chat_id = ?", (page_number, current_page_message_id, chat_id))
        conn.commit()

        # Закрытие соединения
        conn.close()
        callback_query.data = f'page_{current_page}'

        # Теперь можно обновить данные в функции get_data с использованием chat_id, current_page и current_page_message_id
        await get_data(callback_query.message,just='responce')


    elif action == 'view-chat':
        # Обработка действия "Посмотреть чат"
        resp = get_user_id(callback_query.message.chat.id)  # Получаем client_id
        token = get_token(callback_query.message.chat.id)
        data = await get_avito_messages(user_id=resp, chat_id=chat_id, token=token)
        messages = data['messages'][:10]  # Получаем все сообщения чата
        resp = get_user_id(callback_query.message.chat.id)  # Получаем client_id


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

        await mark_chat_as_read(resp, chat_id, token=token)
        # Отправляем объединенный текстовый чат
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message^{user_id}^{chat_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'send^{user_id}^{chat_id}'))
        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=chat_text,
        parse_mode='html',
        reply_markup=keyboard
    )



    elif action == 'send-message':
        user_id, chat_id = action_data[1], action_data[2]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        
        now_button = types.InlineKeyboardButton("Сейчас", callback_data=f'send-now^{chat_id}^{user_id}')
        working_hours_button = types.InlineKeyboardButton("Рабочее время", callback_data=f'send-working-hours^{chat_id}^{user_id}')
        custom_time_button = types.InlineKeyboardButton("В определенное время", callback_data=f'send-custom-time^{chat_id}^{user_id}')
        
        keyboard.add(now_button, working_hours_button, custom_time_button)
        
        await bot.send_message(callback_query.message.chat.id, "Выберите способ отправки сообщения:", reply_markup=keyboard)
    # Получаем chat_id и user_id из callback_data




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send-working-hours^'))
async def send_working_hours(callback_query: types.CallbackQuery, state: FSMContext):
    action_data = callback_query.data
    action_data = callback_query.data.split('^')
    user_id, chat_id = action_data[0], action_data[1] 
    await bot.send_message(callback_query.message.chat.id, "Введите текст сообщения:")

    # Устанавливаем состояние, чтобы ожидать ответа пользователя
    await WorkTimeMessage.waiting_for_text.set()

    # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
    async with state.proxy() as data:
        data['chat_id'] = chat_id
        data['user_id'] = user_id
        data['telegram_chat_id'] = callback_query.message.chat.id  # Добавляем chat_id Telegram чата


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send-custom-time^'))
async def send_custom_time(callback_query: types.CallbackQuery, state: FSMContext):
    action_data = callback_query.data
    action_data = callback_query.data.split('^')
    user_id, chat_id = action_data[0], action_data[1] 
    await bot.send_message(callback_query.message.chat.id, "Введите текст сообщения:")

    # Устанавливаем состояние, чтобы ожидать ответа пользователя
    await SpecificTimeMessage.waiting_for_text.set()

    # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
    async with state.proxy() as data:
        data['chat_id'] = chat_id
        data['user_id'] = user_id
        data['telegram_chat_id'] = callback_query.message.chat.id  # Добавляем chat_id Telegram чата


@dp.message_handler(state=WorkTimeMessage.waiting_for_text)
async def process_time(message: Message, state: FSMContext):
    try:
        # Получаем текст сообщения от пользователя
        response_text = message.text

        # Сохраняем текст сообщения в состоянии
        async with state.proxy() as data:
            chat_id = data['chat_id']
            
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()

            cursor.execute('SELECT start_time, end_time, week_days  FROM time_msgs WHERE chat_id = ?', (message.chat.id,))
            lst = cursor.fetchone()
            cursor.execute('INSERT INTO check_work_msgs (chat_id, start_time, end_time,week_days , avito_chat, response_text) VALUES (?, ?, ?, ?, ?, ?)',
                            (message.chat.id, lst[0], lst[1], lst[2] ,chat_id, response_text))
            conn.commit()
            conn.close()
            await bot.send_message(message.chat.id,'Сообщение добавлено в базу запланированнах для оптравки в рабочее время')
            await state.finish()
        # Переход к следующему состоянию ожидания времени
    except Exception as e:
        await bot.send_message(message.chat.id, "Произошла ошибка при обработке текста сообщения.")
        await state.finish()


@dp.message_handler(state=SpecificTimeMessage.waiting_for_text)
async def process_time(message: Message, state: FSMContext):
    try:
        # Получаем текст сообщения от пользователя
        response_text = message.text

        # Сохраняем текст сообщения в состоянии
        async with state.proxy() as data:
            data['response_text'] = response_text

        await bot.send_message(message.chat.id, "Пожалуйста, введите время в формате HH:MM (например, 14:30).")

        # Переход к следующему состоянию ожидания времени
        await SpecificTimeMessage.next()
    except Exception as e:
        await bot.send_message(message.chat.id, "Произошла ошибка при обработке текста сообщения.")

@dp.message_handler(lambda message: message.text and ":" in message.text, state=SpecificTimeMessage.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    try:
        # Получаем время от пользователя
        user_time = message.text
        # Разбиваем строку с временем на часы и минуты
        hours, minutes = map(int, user_time.split(':'))
        
        # Проверяем, что время валидно (например, часы от 0 до 23, минуты от 0 до 59)
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            async with state.proxy() as data:
                chat_id = data['chat_id']
                user_id = data['user_id']
                telegram_chat_id = data['telegram_chat_id']
                response_text = data['response_text']

                conn = sqlite3.connect('my_database.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO specific_msgs_time (chat_id, time, avito_chat, response_text) VALUES (?, ?, ?, ?)',
                                (message.chat.id, user_time, chat_id, response_text))
                conn.commit()
                conn.close()

                # Отправляем уведомление о успешной отправке сообщения
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-message^{user_id}^{chat_id}'))
                keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{user_id}^{chat_id}'))

                await bot.send_message(
                    chat_id=telegram_chat_id,
                    text='Сообщение успешно добавлено в список ожидаемых для отправки',
                    parse_mode='html',
                    reply_markup=keyboard
                )
                # Завершаем состояние
                await state.finish()
        else:
            await bot.send_message(telegram_chat_id, "Время введено некорректно. Пожалуйста, введите время в формате HH:MM.")
    except Exception as e:
        await bot.send_message(telegram_chat_id, "Произошла ошибка при обработке времени. Пожалуйста, введите время в формате HH:MM.")




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send-working-hours^'))
async def send_working_hours(callback_query: types.CallbackQuery,state: FSMContext):
    action_data = callback_query.data
    action_data = callback_query.data.split('^')
    user_id, chat_id = action_data[0], action_data[1]
        # Запрашиваем текст у пользователя
    await bot.send_message(callback_query.message.chat.id, "Введите текст сообщения:")

    # Устанавливаем состояние, чтобы ожидать ответа пользователя
    await SpecificTimeMessage.waiting_for_text.set()

    # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
    async with state.proxy() as data:
        data['chat_id'] = chat_id
        data['user_id'] = user_id
        data['telegram_chat_id'] = callback_query.message.chat.id  # Добавляем chat_id Telegram чата





@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send-now^'))
async def send_now(callback_query: types.CallbackQuery,state: FSMContext):
    action_data = callback_query.data
    print(action_data)
    chat_text = ''
    action_data = callback_query.data.split('^')
    user_id, chat_id = action_data[0], action_data[1]
    print(user_id,chat_id)
    # Запрашиваем текст у пользователя
    await bot.send_message(callback_query.message.chat.id, "Введите текст сообщения:")

    # Устанавливаем состояние, чтобы ожидать ответа пользователя
    await MyStates.waiting_for_text.set()

    # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
    async with state.proxy() as data:
        data['chat_id'] = chat_id
        data['user_id'] = user_id
        data['telegram_chat_id'] = callback_query.message.chat.id  # Добавляем chat_id Telegram чата


@dp.message_handler(state=TimeMessage.waiting_for_text)
async def process_text2(message: Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        user_id = data['user_id']
        telegram_chat_id = data['telegram_chat_id']  # Получаем chat_id Telegram чата
        # Отправляем текстовое сообщение в чат с пользователем
        resp = get_user_id(message.chat.id)  # Получаем client_id
        token = get_token(message.chat.id)
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT start_time, end_time , week_days FROM time_msgs WHERE chat_id = ?', (message.chat.id,))
        lst = cursor.fetchone()
        cursor.execute('INSERT INTO check_work_msgs (chat_id, start_time, end_time, avito_chat ,response_text) VALUES (?, ?, ?, ?, ?, ?)',
                            (message.chat.id, lst[0], lst[1], lst[2] ,chat_id ,message.text))
        conn.commit()
        conn.close()
        # Отправляем уведомление о успешной отправке сообщения
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-message^{user_id}^{chat_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{user_id}^{chat_id}'))

        await bot.send_message(
            chat_id=telegram_chat_id,  # Используйте chat_id чата с пользователем
            text='Сообщение успешно добавлено в список ожидаемых для отправки',
            parse_mode='html',
            reply_markup=keyboard
        )
    # Завершаем состояние
    await state.finish()


@dp.message_handler(state=MyStates.waiting_for_text)
async def process_text3(message: Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        telegram_chat_id = data['telegram_chat_id']  # Получаем chat_id Telegram чата
        # Отправляем текстовое сообщение в чат с пользователем
        resp = get_user_id(message.chat.id)  # Получаем client_id
        token = get_token(message.chat.id)
        user_id = get_user_id(message.chat.id)
        try:
            await send_message(chat_id=chat_id, user_id=resp, text=message.text, token=token)
            await mark_chat_as_read(resp, chat_id, token=token)
            
            # Отправляем уведомление о успешной отправке сообщения
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-message^{user_id}^{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{user_id}^{chat_id}'))
            await bot.send_message(
                chat_id=telegram_chat_id,  # Используйте chat_id чата с пользователем
                text='Сообщение отправлено успешно!',
                parse_mode='html',
                reply_markup=keyboard
            )
        except:
            await bot.send_message(
                chat_id=telegram_chat_id,
                text='Сообщение не отправлено. Пожалуйста, попробуйте еще раз.',
                parse_mode='html'
            )
    # Завершаем состояние
    await state.finish()


@dp.message_handler(content_types=types.ContentTypes.TEXT, chat_type=types.ChatType.GROUP)
async def check_pattern(message: types.Message):
    if message.text.startswith("Шаблон:"):
        # Если сообщение начинается с "Шаблон", выполните нужные действия
        lst = message.text.split('\n')
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        try:
            # Проверяем существование записи с указанным chat_id
            cursor.execute('SELECT id FROM chats WHERE chat_id = ?', (message.chat.id,))
            existing_chat = cursor.fetchone()
            if existing_chat != None:
                cursor.execute('SELECT id, test_period FROM chats WHERE chat_id = ?', (message.chat.id,))
                time = cursor.fetchone()
                test_period_str = time[1]
                test_period_str = test_period_str.split('.')[0]  # Отбрасываем дробную часть секунды
                test_period = datetime.datetime.strptime(test_period_str, '%Y-%m-%d %H:%M:%S')
                if test_period <= datetime.datetime.now():
                    keyboard = types.InlineKeyboardMarkup()
                    sum = get_sum(tg_id=message.chat.id)
                    keyboard.add(types.InlineKeyboardButton(text='Продлить подписку',url=sum))
                    await message.reply(f"Ваш тестовый период истек. Для продолжения работы, пожалуйста оплатите подписку",reply_markup=keyboard)
                else:
                    token = set_personal_token(client_id=lst[2],client_secret=lst[3])
                    if token:
                    # Обновляем существующую запись в таблице chats
                        cursor.execute('UPDATE chats SET id_avito = ?, client_id = ?, client_secret = ?, token = ?  WHERE chat_id = ?',
                                    (lst[1], lst[2], lst[3], token, message.chat.id))
                        conn.commit()
                        await bot.send_message(message.chat.id,'Данные успешно обновлены')
                    else:
                        await bot.send_message(message.chat.id,'Вы неправильно вставили данные, пожалуйста следуйте инструкции')

            else:
                if test_period <= datetime.datetime.now():
                    keyboard = types.InlineKeyboardMarkup()
                    sum = get_sum(tg_id=message.chat.id)
                    keyboard.add(types.InlineKeyboardButton(text='Продлить подписку',url=sum))
                    await message.reply(f"Ваш тестовый период истек. Для продолжения работы, пожалуйста оплатите подписку",reply_markup=keyboard)
                else:
                    token = set_personal_token(client_id=lst[2],client_secret=lst[3])
                    if token:
                        # Если запись не существует, создаем новую
                        cursor.execute('INSERT INTO chats (chat_id, id_avito, client_id, client_secret,token) VALUES (?, ?, ?, ?, ?)',
                                    (message.chat.id, lst[1], lst[2], lst[3], token))
                        
                        conn.commit()
                        await bot.send_message(message.chat.id,'Avito успешно подключен, теперь сообщения будут приходить в этот чат.')
                    else:
                        await bot.send_message(message.chat.id,'Вы неправильно вставили данные, пожалуйста следуйте инструкции')

                   
            
            # Сохраняем изменения в базе данных


        except:
            pass
            
        # Закрываем соединение
        conn.close()

    else:
        # Если сообщение не начинается с "Шаблон", можно выполнить другие действия или проигнорировать его
        await message.reply("Сообщение не начинается с 'Шаблон'.")

# Обработчик команды /account_info
@dp.message_handler(commands=['account_info'])
async def get_account_info(message: types.Message):
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="🔎 Посмотреть баланс", callback_data=f'view_balance'),types.InlineKeyboardButton(text="✍️ Изменить сумму ", callback_data=f'chang_balance'))
        keyboard.add(types.InlineKeyboardButton(text='⁒ Изменить процент подписки',callback_data='change_procent'))
        keyboard.add(types.InlineKeyboardButton(text="🕸 Посмотореть ссылку для оплаты ", url='https://yoomoney.ru/transfer/quickpay?requestId=353339313234373332315f64636536343062613739396163313832353138336465376132343935653739633136313830646464'))
        keyboard.add(types.InlineKeyboardButton(text='Посмотреть статиску',callback_data='show_statistic'))
        keyboard.add(types.InlineKeyboardButton(text='Поменять тариф',callback_data='change_tarif'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'main_back'))
        await bot.send_message(message.chat.id, 'Выберите опцию', reply_markup=keyboard)
    except Exception as e:
        print('Error:', str(e))




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('view_balance',  'show_statistic' , 'change_tarif' ,'chang_balance','view_site','change_procent')))
async def action_callback(callback_query: types.CallbackQuery,state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='acc_back'))  # Update this line
    if callback_query.data == 'view_balance':
        try:

                    # Получаем информацию из ЮMoney
            user = client.account_info()
            account_info = (
                f"Номер карты: <strong >{user.account}</strong>\n"
                f"Баланс: {user.balance} ₽\n"

            )
            # Отправляем информацию в Telegram
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=account_info, parse_mode='html',reply_markup=keyboard)
            await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        except Exception as e:
            await callback_query.message.reply(f"An error occurred: {str(e)}")
    elif callback_query.data == 'change_tarif':
        global users_per_page_2
        global current_page_2
        global total_pages_2
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        chat_id = callback_query.message.chat.id
        cursor.execute("SELECT chat_id, acc_id, test_period FROM chats")
        subscriptions = cursor.fetchall()
        current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S.%f")

        # Number of users to display per page

        # Calculate the total number of pages
        total_pages_2 = int(ceil(len(subscriptions) / users_per_page_2))

        # Current page (you can set this based on user input)

        # Calculate the index range for the current page
        start_index = (current_page_2 - 1) * users_per_page_2
        end_index = min(current_page_2 * users_per_page_2, len(subscriptions))

        # Create the inline keyboard
        keyboard = types.InlineKeyboardMarkup()

        # Add users for the current page
        for i in range(start_index, end_index):
            subscription = subscriptions[i]
            time = datetime.datetime.strptime(subscription[2], '%Y-%m-%d %H:%M:%S.%f')
            acc_id = subscription[1]
            cursor.execute("SELECT id_telegram FROM clients WHERE id = ?", (acc_id,))
            id_telegram = cursor.fetchone()
            user = await bot.get_chat(id_telegram[0])

            if time >= current_time:
                button_text = f'{user.username} ✅'
            else:
                button_text = f'{user.username} ❌'

            button = types.InlineKeyboardButton(text=button_text, callback_data=f"select_user_{subscription[0]}")
            keyboard.add(button)

        # Add "Next" and "Back" buttons for pagination
        if current_page_2 > 1:
            keyboard.add(types.InlineKeyboardButton(text='Back', callback_data=f'prev_page_{current_page_2 - 1}'))
        if current_page_2 < total_pages_2:
            keyboard.add(types.InlineKeyboardButton(text='Next', callback_data=f'next_page_{current_page_2 + 1}'))

        # Add a "Return" button
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='acc_back'))

        # Send the message with the inline keyboard
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='Выберите человека', parse_mode='html',reply_markup=keyboard)

        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную


    elif callback_query.data == 'show_statistic':
        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()

            # Получите chat_id пользователя
            chat_id = callback_query.message.chat.id

            # Получите информацию о подписках из базы данных
            cursor.execute("SELECT chat_id, acc_id, test_period FROM chats")
            subscriptions = cursor.fetchall()
            current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            current_time = datetime.datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S.%f")

            if subscriptions:

                message = "<b>Активные подписки:</b>\n\n"
                for subscription in subscriptions:
                    time = datetime.datetime.strptime(subscription[2], '%Y-%m-%d %H:%M:%S.%f')
                    if time>=current_time:
                        acc_id = subscription[1]
                        print(acc_id)
                        cursor.execute("SELECT id_telegram FROM clients WHERE id = ?",(acc_id,))
                        id_telegram = cursor.fetchone()
                        print(id_telegram)
                        user = await bot.get_chat(id_telegram[0])
                        
# Parse the datetime string with seconds but without fractional seconds
# Parse the datetime string with seconds but without fractional seconds
                        test_period = datetime.datetime.strptime(subscription[2], '%Y-%m-%d %H:%M:%S.%f')

                        # Format the test_period for output with date and time without seconds and fractional seconds
                        formatted_test_period = test_period.strftime('%Y-%m-%d %H:%M')
                        message += f"Аккаунт <a href = '{user.user_url}'>{user.username}:</a> до {formatted_test_period}\n"
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Вернуться назад',callback_data='acc_back'))

                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=message, parse_mode='html',reply_markup=keyboard)
                await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

            else:
                await bot.send_message(chat_id, 'У вас нет активных подписок.')

        except Exception as e:
            print('Error:', str(e))
        finally:
            # Важно закрыть соединение с базой данных после выполнения операций
            conn.close()



    elif callback_query.data == 'chang_balance':
        await bot.send_message(callback_query.from_user.id, "Введите сумму подписки:")
        # Устанавливаем состояние, чтобы ожидать ответа пользователя
        await YooMoneySum.waiting_fot_sum.set()

    elif callback_query.data == 'change_procent':
        await bot.send_message(callback_query.from_user.id, "Введите процент скидки:")
        # Устанавливаем состояние, чтобы ожидать ответа пользователя
        await YooMoneyProcent.waiting_fot_procent.set()  
    else:
        pass

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('select_user_')))
async def current_us(callback_query: types.CallbackQuery, state: FSMContext):
    action_data = callback_query.data.split('_')
    await bot.send_message(callback_query.message.chat.id,'Введите кол-во дней для добавления в тариф пользователя')
    await UpdateDaysState.waiting_for_days.set()
    await state.update_data(user_id=action_data[2])


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'acc_back')
async def back_acc(callback_query: types.CallbackQuery):
    print('dont ')
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="🔎 Посмотреть баланс", callback_data=f'view_balance'),types.InlineKeyboardButton(text="✍️ Изменить сумму ", callback_data=f'chang_balance'))
        keyboard.add(types.InlineKeyboardButton(text='⁒ Изменить процент подписки',callback_data='change_procent'))
        keyboard.add(types.InlineKeyboardButton(text="🕸 Посмотореть ссылку для оплаты ", url='https://yoomoney.ru/transfer/quickpay?requestId=353339313234373332315f64636536343062613739396163313832353138336465376132343935653739633136313830646464'))
        keyboard.add(types.InlineKeyboardButton(text='Посмотреть статиску',callback_data='show_statistic'))
        keyboard.add(types.InlineKeyboardButton(text='Поменять тариф',callback_data='change_tarif'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'main_back'))
        
        # Use edit_message_text to edit the message with the updated keyboard markup
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите опцию',
            reply_markup=keyboard,
        )
    except Exception as e:
        print('Error:', str(e))


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'main_back')
async def main_back(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    print(callback_query.message.chat.id)
    if callback_query.message.chat.id in admin_ids:
        keyboard.add(
            types.InlineKeyboardButton(text='🎥 Видео', callback_data='video'),
            types.InlineKeyboardButton(text='📋 Список аккаунтов', callback_data='spisok')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='🤖 Автоответы', callback_data='auto_answera'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='sos')
    )
        keyboard.add(types.InlineKeyboardButton(text='Админ панель',callback_data='acc_back'))
    else:
        keyboard.add(
            types.InlineKeyboardButton(text='🎥 Видео', callback_data='video'),
            types.InlineKeyboardButton(text='📋 Список аккаунтов', callback_data='spisok')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='🤖 Автоответы', callback_data='auto_answera'),
            types.InlineKeyboardButton(text='❓ Помощь', callback_data='sos')
    )
    await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    ) 


@dp.message_handler(state=UpdateDaysState.waiting_for_days)
async def update_days(message: Message, state: FSMContext):
    try:
        days = int(message.text)  # Assuming the user enters a valid integer for days
        user_data = await state.get_data()
        user_id = user_data.get('user_id', None)
        print(user_id)
        print('иииув')
        # Update the database with the new number of days for the user
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT test_period FROM chats WHERE chat_id = ?", (user_id,))
        current_test_period = cursor.fetchone()[0]

        # Convert the current_test_period to a datetime object
        current_test_period = datetime.datetime.strptime(current_test_period, '%Y-%m-%d %H:%M:%S.%f')

        # Add the number of days to the current date
        new_test_period = current_test_period + datetime.timedelta(days=days)
        cursor.execute("UPDATE chats SET test_period = ? WHERE chat_id = ?", (new_test_period, user_id))
        conn.commit()
        conn.close()

        await message.reply(f"Successfully updated the number of days to {days} for user {user_id}")
    except ValueError:
        await message.reply("Please enter a valid integer for the number of days.")

    # Finish the state
    await state.finish()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('prev_page_', 'next_page_')))
async def pagination_callback(callback_query: types.CallbackQuery, state: FSMContext):
    page_number = int(callback_query.data.split('_')[2])
    global users_per_page_2
    global current_page_2
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    chat_id = callback_query.message.chat.id
    cursor.execute("SELECT chat_id, acc_id, test_period FROM chats")
    subscriptions = cursor.fetchall()
    current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S.%f")
    if callback_query.data.startswith('prev_page_'):
        current_page_2 = max(current_page_2 - 1, 1)
    elif callback_query.data.startswith('next_page_'):
        current_page_2 = min(current_page_2 + 1, total_pages_2)

    # Calculate the index range for the current page
    start_index = (current_page_2 - 1) * users_per_page_2
    end_index = min(current_page_2 * users_per_page_2, len(subscriptions))

    # Create the updated inline keyboard
    updated_keyboard = types.InlineKeyboardMarkup()

    # Add users for the current page
    for i in range(start_index, end_index):
        subscription = subscriptions[i]
        time = datetime.datetime.strptime(subscription[2], '%Y-%m-%d %H:%M:%S.%f')
        acc_id = subscription[1]
        cursor.execute("SELECT id_telegram FROM clients WHERE id = ?", (acc_id,))
        id_telegram = cursor.fetchone()
        user = await bot.get_chat(id_telegram[0])

        if time >= current_time:
            button_text = f'{user.username} ✅'
        else:
            button_text = f'{user.username} ❌'

        button = types.InlineKeyboardButton(text=button_text, callback_data=f"select_user_{user.id}")
        updated_keyboard.add(button)

    # Add "Back" and "Next" buttons for pagination
    if current_page_2 > 1:
        updated_keyboard.add(types.InlineKeyboardButton(text='Back', callback_data=f'prev_page_{current_page_2 - 1}'))
    if current_page_2 < total_pages_2:
        updated_keyboard.add(types.InlineKeyboardButton(text='Next', callback_data=f'next_page_{current_page_2 + 1}'))

    # Add a "Return" button
    updated_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='acc_back'))

    # Edit the existing message to update the user interface
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=updated_keyboard)



@dp.message_handler(state=YooMoneyProcent.waiting_fot_procent)
async def process_proc(message: Message, state: FSMContext):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='acc_back'))  # Update this line
        # Получаем введенную пользователем сумму
        user_input = message.text
        # Преобразуем введенный текст в число (проверьте, что это число)
        sum_to_set = float(user_input)

        # Изменяем сумму в Quickpay
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id

        # SQL-запрос для выбора client_id по id_telegram
        cursor.execute("UPDATE payment SET procent = ?, telegram_id = ?",(sum_to_set,message.from_user.id))
        conn.commit()
        # Отправляем сообщение с новой суммой и ссылкой на оплату
        await message.answer(f"Процент скидки изменили на {sum_to_set}%.",reply_markup=keyboard)

        # Завершаем состояние ожидания
        await state.finish()

    except ValueError:
        await message.answer("Пожалуйста, введите корректное числовое значение для процентной скидки.")

@dp.message_handler(state=YooMoneySum.waiting_fot_sum)
async def process_sum(message: Message, state: FSMContext):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='acc_back'))  # Update this line
        # Получаем введенную пользователем сумму
        user_input = message.text
        # Преобразуем введенный текст в число (проверьте, что это число)
        sum_to_set = float(user_input)

        # Изменяем сумму в Quickpay
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id

        # SQL-запрос для выбора client_id по id_telegram
        cursor.execute("UPDATE payment SET paysum = ?, telegram_id = ?",(sum_to_set,message.from_user.id))
        conn.commit()
        # Отправляем сообщение с новой суммой и ссылкой на оплату
                # Отправляем информацию в Telegram
        await message.answer(f"Сумма изменена на {sum_to_set} руб.", reply_markup=keyboard)

        # Завершаем состояние ожидания
        await state.finish()

    except ValueError:
        await message.answer("Пожалуйста, введите корректное числовое значение для суммы.")
# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    text = message.text

    if text.count(' ')==2:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        text = text.replace(' ','')
        # Данные пользователя
        id_telegram = message.chat.id  # Пример id_telegram
        client_id = get_user_id(message.chat.id)   # Пример client_id

        # SQL-запрос для проверки наличия записи с данным id_telegram
        select_query = 'SELECT * FROM clients WHERE id_telegram = ?'
        cursor.execute(select_query, (id_telegram,))

        # Извлечение результата запроса
        existing_record = cursor.fetchone()

        # Если запись существует, обновите её client_id
        if existing_record:
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
        pass
    # Здесь вы можете обрабатывать текстовые сообщения от пользователя
    # и выполнять соответствующие действия


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('view-chat-group^','send-message-group^')))
async def action_callback(callback_query: types.CallbackQuery,state: FSMContext):
    print()
    action_data = callback_query.data
    action_data = callback_query.data.split('^')
    action = action_data[0]
    chat_id = ''
    user_id = ''
    if len(action_data)>2:
        user_id, chat_id= action_data[1], action_data[2]
    else:
        pass
    if action == 'back':
        global current_page  # Declare that we are using the global current_page variable
        global current_page_message_id  # Declare a global variable to store the message ID
        callback_query.data = f'page_{current_page}'
        page_number = int(callback_query.data.split('_')[1])
        current_page = page_number  # Update the current page
        # Trigger a refresh of the data
        await get_data(callback_query.message,just='responce')
    elif action == 'send-message-group':

    # Получаем chat_id и user_id из callback_data
        user_id, chat_id = action_data[1], action_data[2]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        
        now_button = types.InlineKeyboardButton("Сейчас", callback_data=f'send-group-now^{chat_id}^{user_id}')
        working_hours_button = types.InlineKeyboardButton("Рабочее время", callback_data=f'send-working-hours^{user_id}^{chat_id}')
        custom_time_button = types.InlineKeyboardButton("В определенное время", callback_data=f'send-custom-time^{user_id}^{chat_id}')
        
        keyboard.add(now_button, working_hours_button, custom_time_button)
        
        await bot.send_message(callback_query.message.chat.id, "Выберите способ отправки сообщения:", reply_markup=keyboard)
    # Получаем chat_id и user_id из callback_data
        # Запрашиваем текст у пользователя


    elif action == 'view-chat-group':
        # Обработка действия "Посмотреть чат"
        resp = get_user_id(callback_query.message.chat.id)  # Получаем client_id
        token = get_token(callback_query.message.chat.id)
        data = await get_avito_messages(user_id=resp, chat_id=chat_id, token=token)
        chat_text = ""
        messages = data['messages'][:10]  # Получаем все сообщения чата

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

        await mark_chat_as_read(resp, chat_id, token=token)
        # Отправляем объединенный текстовый чат
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message-group^{chat_id}^{user_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'send^{user_id}^{chat_id}'))

        await bot.answer_callback_query(callback_query_id=callback_query.id)  # Отмечаем кнопку как обработанную

        await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=chat_text,
        parse_mode='html',
        reply_markup=keyboard
    )
    






@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send-group-now^'))
async def send_group(callback_query: types.CallbackQuery,state: FSMContext):
    action_data = callback_query.data
    chat_text = ''
    action_data = callback_query.data.split('^')
    user_id, chat_id = action_data[1], action_data[2]

    # Запрашиваем текст у пользователя
    await bot.send_message(callback_query.message.chat.id, "Введите текст сообщения:")

    # Устанавливаем состояние, чтобы ожидать ответа пользователя
    await MyStatesGroup.waiting_for_text.set()

    # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
    async with state.proxy() as data:
        data['chat_id'] = chat_id
        data['user_id'] = user_id
        data['telegram_chat_id'] = callback_query.message.chat.id  # Добавляем chat_id Telegram чата




@dp.message_handler(state=MyStatesGroup.waiting_for_text)
async def process_text4(message: Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        user_id = get_user_id(message.chat.id)
        telegram_chat_id = data['telegram_chat_id']  # Получаем chat_id Telegram чата
        # Отправляем текстовое сообщение в чат с пользователем
        resp = get_user_id(message.chat.id)  # Получаем client_id
        token = get_token(message.chat.id)
        try:
            await send_message(chat_id=chat_id, user_id=resp, text=message.text, token=token)
            await mark_chat_as_read(resp, chat_id, token=token)
            # Отправляем уведомление о успешной отправке сообщения
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-group-now^{user_id}^{chat_id}'))
            keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{user_id}^{chat_id}'))

            await bot.send_message(
                chat_id=telegram_chat_id,  # Используйте chat_id чата с пользователем
                text='Сообщение отправлено успешно!',
                parse_mode='html',
                reply_markup=keyboard
            )
        except:
            await bot.send_message(
                chat_id=telegram_chat_id,
                text='Сообщение не отправлено. Пожалуйста, попробуйте еще раз.',
                parse_mode='html'
            )
    # Завершаем состояние
    await state.finish()

async def get_unread_messages(chat_id):
    avito_id = get_user_id(chat_id)
    token = get_token(chat_id)
    try:
        json_data = await get_unread_messagef_avito(token=token, user_id=avito_id)
        ch_id = ''
        # Создайте список, чтобы отслеживать идентификаторы отправленных сообщений
        sent_message_ids = sent_messages.get(chat_id, [])
                
        
        if "chats" in json_data:
            for chat in json_data["chats"]:
                message_id = chat["last_message"]["id"]
                if message_id not in sent_message_ids:
                    sent_message_ids.append(message_id)
                    sent_messages[chat_id] = sent_message_ids
                    ch_id = chat['id']
                    title = chat["context"]["value"]["title"]
                    price_string = chat["context"]["value"]["price_string"]
                    url = chat["context"]["value"]["url"]
                    city = chat["context"]["value"]["location"]["title"]

                    users = chat["users"]
                    author_name = ""
                    client_name = ""
                    for user in users:
                        if user["id"] == chat["last_message"]["author_id"]:
                            author_name = user["name"]
                        else:
                            client_name = user["name"]

                    last_message_text = chat["last_message"]["content"]["text"]

                    # Создание сообщения
                    response_message = (
                        f"Товар: [{markdown.escape_md(title)} {markdown.escape_md(price_string)}]({url})\n"
                        f"Автор товара: {markdown.escape_md(client_name)}\n"
                        f"Город: {markdown.escape_md(city)}\n"
                        f"Клиент: {markdown.escape_md(author_name)}\n\n"
                        f"Текст сообщения:\n{markdown.escape_md(last_message_text)}\n\n"
                    )
                    
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message-group^{ch_id}^{avito_id}'),types.InlineKeyboardButton(text="💬Посмотреть чат", callback_data=f'view-chat-group^{avito_id}^{ch_id}'))
                    await bot.send_message(chat_id, text=response_message,parse_mode=types.ParseMode.MARKDOWN,reply_markup=keyboard)
    except:
        pass

async def background_task(chat_id):
    while True:
        # Получение всех непрочитанных сообщений
        await get_unread_messages(chat_id)
        await asyncio.sleep(5)  # Подождите 5 секунд перед повторным выполнением

async def process_msgs_data(token, avito_id, data, current_day_ru):
    unread_messages = await get_unread_messagef_avito(token=token, user_id=avito_id)
    available_days = [day.strip() for day in data[4].split(',')]
    
    if current_day_ru in available_days and unread_messages:
        for message in unread_messages.get("chats", []):
            chat_id = message['id']
            response_text = ''
            lst_messages = ''
            
            try:
                lst_messages =  await get_lst_messages_v3_async(token=token, user_id=avito_id, chat_id=chat_id)
                response_text = find_matching_answer()
            except Exception as e:
                print(f"Error in answer: {e}")
                continue
            
            
            if response_text and len(lst_messages["messages"]) == 1:
                try:
                    await send_message(chat_id=chat_id, user_id=avito_id, text=response_text, token=token)
                    await mark_chat_as_read(avito_id, chat_id, token=token)
                except Exception as e:
                    print(f"Error sending message: {e}")

async def process_time_msgs_data(token, avito_id, data, current_day_ru):
    current_date = datetime.datetime.now().date()
    unread_messages = await get_unread_messagef_avito(token=token, user_id=avito_id)
    available_days = [day.strip() for day in data[4].split(',')]
    start_time = datetime.datetime.strptime(data[-2], '%H:%M').time()
    end_time = datetime.datetime.strptime(data[-1], '%H:%M').time()

    if current_day_ru in available_days and unread_messages:
        for message in unread_messages.get("chats", []):
            chat_id = message['id']
            response_text = ''
            message_created = datetime.datetime.fromtimestamp(message['created']).time()
            
            try:
                msg = await get_lst_messages_v3_async(token=token, user_id=avito_id, chat_id=chat_id)
                response_text = find_matching_answer_work()
            except Exception as e:
                print(f"Error in answer: {e}")
                continue
            
            today_messages = sum(1 for m in msg['messages'] if datetime.datetime.fromtimestamp(m['created']).date() == current_date)
            
            if start_time <= message_created <= end_time and today_messages == 1:
                try:
                    await send_message(chat_id=chat_id, user_id=avito_id, text=response_text, token=token)
                    await mark_chat_as_read(avito_id, chat_id, token=token)
                except Exception as e:
                    print(f"Error in answer: {e}")
                    continue
            else:
                if today_messages == 1:
                    try:
                        await send_message(chat_id=chat_id, user_id=avito_id, text='Здравствуйте, спасибо за обращение, попытаемся ответить как можно скорее в начале рабочего дня 🕥', token=token)
                        await mark_chat_as_read(avito_id, chat_id, token=token)
                    except Exception as e:
                        print(f"Error in answer: {e}")
                        continue



async def send_unread_triggers():
    while True:
        
        chat_data = get_chats_with_triggers()
        msgs = get_chats_with_msgs()
        time_msgs = get_chats_with_time_msgs()
        current_day = datetime.datetime.now().strftime("%a").upper()        
        # Преобразуйте текущий день в русский формат, используя словарь
        current_day_ru = day_mapping.get(current_day, current_day)
        for chat_id in chat_data:
            test = get_time2(chat_id[1]) 
            if test and chat_id[3]:

                token = get_token(chat_id[1])
                avito_id = get_user_id(chat_id[1])

                unread_messages = await get_unread_messagef_avito(token=token,user_id=avito_id)  # Асинхронная обработка непрочитанных сообщений
                if unread_messages:
        
                    for message in unread_messages["chats"]:
                        user_text = message["last_message"]["content"]["text"]
                        trigger, response_text = find_matching_trigger(user_text)
                        if trigger and response_text:
                            await send_message(avito_id, message["id"] ,response_text, token)
                            await mark_chat_as_read(avito_id, chat_id[0], token)
                            await bot.send_message(chat_id[0], text='Автоматический ответ отправлен')

        for data in msgs:
          
            test = get_time2(data[2])
            if test and data[3]:
                token = get_token(data[2])
                avito_id = get_user_id(data[2])
                await process_msgs_data(token, avito_id, data, current_day_ru)
        for data in time_msgs:
            test = get_time2(data[2])
            if test and data[3]:
                token = get_token(data[2])
                avito_id = get_user_id(data[2])
                await process_time_msgs_data(token, avito_id, data, current_day_ru)

        await asyncio.sleep(7)
                                    


async def process_chats_with_data():
    while True:
    # Получите чаты из базы данных, где заполнены avito_id, client_id, client_secret и token
        conn = sqlite3.connect('my_database.db')
        data = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT chat_id FROM chats")
            data = cursor.fetchall()
            conn.close() 
        except:
            pass
        chats_with_data = get_chats_with_data()

        for chat in chats_with_data:
            chat_id = chat[0]
            # Выполните обработку поиска новых сообщений и отправку сообщений для этого чата
            test = get_time2(chat_id)
            if test:
                try:
                    await get_unread_messages(chat_id)
                except Exception as e:
                    print(f"Error in get_unread_messages: {e}")

        await asyncio.sleep(5)

async def check_work_msgs():
    while True:
        current_time_str = datetime.datetime.now().strftime("%H:%M")
        current_time = datetime.datetime.strptime(current_time_str, "%H:%M").time()
        current_day = day_mapping[datetime.datetime.now().strftime("%a").upper()]
        conn = sqlite3.connect('my_database.db')
        data = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT chat_id, start_time, end_time, avito_chat, response_text, week_days,id FROM check_work_msgs")
            data = cursor.fetchall()
            conn.close() 
        except:
            pass
        if data:
            for item in data:
                test = get_time2(item[0])
                if test:

                    user_id = get_user_id(item[0])
                    token = get_token(item[0])
                    start_time = datetime.datetime.strptime(item[1], '%H:%M').time()
                    end_time = datetime.datetime.strptime(item[2], '%H:%M').time()
                    if start_time <= current_time <= end_time and current_day in item[-2]:
                        await send_message(chat_id=item[3], user_id=user_id, text=item[-2], token=token)
                        await mark_chat_as_read(user_id, item[3], token=token)
                        await bot.send_message(chat_id=item[0], text='Запланированное сообщение отправлено')
                        clear_check_work_msgs(item[-1])    

                    else:
                        print('No scheduled message for this time or day')

        await asyncio.sleep(2)

async def specific_time():
    while True:
        current_time_str = datetime.datetime.now().strftime("%H:%M")
        current_time = datetime.datetime.strptime(current_time_str, "%H:%M").time()
        conn = sqlite3.connect('my_database.db')
        data = None
        count = 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT chat_id,time,avito_chat,response_text FROM specific_msgs_time")
            data = cursor.fetchall()
            conn.close() 
        except:
            pass
        if data:
            for item in data:
                test = get_time2(item[0])
                if test:
                    user_id = get_user_id(item[0])
                    token = get_token(item[0])
                    time = datetime.datetime.strptime(item[1], '%H:%M').time()
                    if time == current_time:

                        await send_message(chat_id=item[2], user_id=user_id, text=item[-1], token=token)
                        await mark_chat_as_read(user_id, item[2], token=token)
                        await bot.send_message(chat_id=item[0],text='Запланированное сообщение отправлено')
                        clear_specific_msgs_time(item[2]) 

                    else:
                        print('nooo specific')
        await asyncio.sleep(2)


async def update_tokens_periodically():
    while True:
        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT chat_id,client_id,client_secret FROM chats")
            data = cursor.fetchall()
            conn.close()
            test = get_time(data[0])
            if test:
                for chat in data:
                    await update_token_for_chat(chat[0],chat[1],chat[2])
            # Ждите 24 часа перед следующим обновление
        except:
            pass
        await asyncio.sleep(24 * 3600)  # 24 часа в секундах

if __name__ == '__main__':
    make_db()
    insert_initial_data()

    # loop = asyncio.get_event_loop()

    # loop.create_task(update_tokens_periodically())
    # loop.create_task(check_work_msgs())
    # loop.create_task(specific_time())
    # # Запустите задачу для обработки чатов с данными
    # loop.create_task(process_chats_with_data())

    # loop.create_task(send_unread_triggers())
    

    
    executor.start_polling(dp, skip_updates=True)