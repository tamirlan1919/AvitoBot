import json
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import time
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
from yoomoney import Client
import os
from aiogram import types
from aiogram.utils import exceptions
from money_cart import get_sum
import json
import schedule
from aiogram.dispatcher.filters import Command, ChatTypeFilter
yoomoney_token = "4100117394518969.25C11A278171A9D98CF57B29E20869FE7175F8E5F0D82C642CB12B819214769229B792D693CD7A205D5D8B524294B1E710CECA73FB581A110CD748405B3A3709592F767FB683ACCE256C92453C4EA831F0E9EBA02063DF8DBA8728EE9B2A2CC60AA1EAD2AF79160F273D90F23C06E6E66B7B874261A33FD1BBA66C0A96297EAD"

client = Client(yoomoney_token)
# Ваш токен Telegram-бота
BOT_TOKEN = '6515821471:AAFspRJMRcCFfJP8-g9WRGS02jK-aydFsBo'




# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
memory_storage = MemoryStorage()  # Инициализируем MemoryStorage
dp = Dispatcher(bot,storage=memory_storage)
dp.middleware.setup(LoggingMiddleware())
sent_messages = {}


current_page = 0
current_page_message_id = None  # Инициализация переменной


current_page2 = 0
current_page_message_id2 = None

# Создаем множество для хранения уникальных имен пользователей
unique_user_names = set()
image_folder = 'images/test_period'


async def check_new_messages(message:types.Message):
    while True:
        # Здесь вы можете добавить логику для проверки наличия новых сообщений.
        user_id = get_user_id(message.chat.id)
        token = get_token(message.chat.id)
        avito_data = get_avito_unread_data(token=token, user_id=user_id)
        
        if avito_data and 'users' in avito_data:
            new_message_count = len(avito_data['users'])
            if new_message_count > 0:
                # Если есть новые сообщения, выполните необходимые действия,
                # например, уведомьте администратора или обработайте их.
                await bot.send_message(message.chat.id, f'Новых сообщений: {new_message_count}')
        
        await asyncio.sleep(10)  # Подождите 10 секунд перед следующей проверкой (или укажите другой интервал)

@dp.message_handler(Command("start") & ChatTypeFilter(types.ChatType.PRIVATE))
async def start(message: types.Message):
    text = '''Бот работает с использованием официальных API-ключей, которые предоставляются после перевода вашего аккаунта на тип "КОМПАНИЯ". Важно отметить, что бот не будет функционировать с аккаунтом типа "ЧАСТНОЕ ЛИЦО". Бот поддерживает работу в любом выбранном вами тарифе.

Если у вас есть небольшое количество объявлений и ваш аккаунт на данный момент настроен как "ЧАСТНОЕ ЛИЦО", вам следует связаться с поддержкой Авито по номеру 8 800 600 00 01 и запросить изменение типа аккаунта на "КОМПАНИЯ". После этого вы сможете подключить любой тариф и получить доступ к API-ключам.

Важно помнить, что после перехода на тип "КОМПАНИЯ" вы будете обязаны подключить тариф с оплатой за просмотры, и обратное возвращение к бесплатным размещениям будет невозможным.

Желаем вам приятного использования бота. Если у вас возникнут вопросы, не стесняйтесь обращаться в нашу поддержку, доступную по ссылке @timaadev'''
    await bot.send_message(message.chat.id,text=text)
    with open('video.mp4', 'rb') as video_file:
        await bot.send_video(chat_id=message.chat.id, video=video_file)
    text1 = '''ИНСТРУКЦИЯ №1 ❗️❗️❗️

В этом видео вы научитесь:

1.Создавать папку для того, чтобы было удобно работать и все чаты были у вас на виду

2.Создавать группу и добавлять бота (SK2) - не забудьте бота назначить АДМИНИСТАТОРОМ⚠️

Дальнейшую инструкцию Вы найдете при создании "Любой группы" после нажатия "/start"'''
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
    keyboard.add(types.InlineKeyboardButton(text='📹Видеоинструкция', callback_data='video'),
                 types.InlineKeyboardButton(text='📓Cписок подключенных аккаунтов', callback_data='spisok'))
    keyboard.add(types.InlineKeyboardButton(text='🤖Автоответы', callback_data='auto_answera'),
                 types.InlineKeyboardButton(text='🆘Помощь', callback_data='sos'))
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


    await bot.send_message(message.chat.id, text=text1,reply_markup=keyboard)

@dp.message_handler(Command("start") & ChatTypeFilter(types.ChatType.GROUP))
async def start_group(message: types.Message):
    chat_id = message.chat.id
    user_id_telegram = message.from_user.id
    # Вставляем запись в таблицу chats
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id FROM clients WHERE id_telegram = ?', (user_id_telegram,))
        user_id = cursor.fetchone()
        if user_id:
            # Проверяем, существует ли запись с такими acc_id и chat_id
            cursor.execute('SELECT id FROM chats WHERE acc_id = ? AND chat_id = ?', (user_id[0], chat_id))
            existing_chat = cursor.fetchone()
            if not existing_chat:
                # Если запись не существует, вставляем новую запись в таблицу chats
                cursor.execute('SELECT test_period_end FROM clients WHERE id = ?', (user_id[0],))
                test_per = cursor.fetchone()
                cursor.execute('INSERT INTO chats (chat_id, acc_id, test_period) VALUES (?, ?, ?)', (chat_id, user_id[0], test_per[0]))
                conn.commit()
            else:
                await bot.send_mes
    except:
        pass

    conn.close()

    text1 = '''ПЕРЕД ИСПОЛЬЗОВАНИЕМ ОБЯЗАТЕЛЬНО ПРОЧТИТЕ❗️❗️❗️

Бот работает через официальные Api ключи, которые выдаются при переводе типа аккаунта на "КОМПАНИЮ" . Бот работает в любом тарифе❗️

ВАЖНО:  с типом "ЧАСТНОЕ ЛИЦО" БОТ работать НЕ  БУДЕТ❗️

Если у вас не много объявлений и подключен тип аккаунта "Частное лицо", то позвоните в поддержку Авито (8 800 600 00 01) и попросите перевести ваш аккаунт на тип "КОМПАНИЯ". После этого нужно будет подключить любой тариф. После подключения Вам будут доступны ключи. 

ВАЖНО❗️Если вы перейдете на тип "КОМПАНИЯ",нужно будет подключить тариф оплату за просмотры,обратно на бесплатные размещения перейти будет НЕ ВОЗМОЖНО❗️

Приятного пользования. С уважением команда SK_Avito_Bot. Будут вопросы, обязательно пишите😊 в нашу поддержку          👉 @Manager_SK2_Avito 👈

Так же попрошу Вас подписаться на мой канал @SK2_Avito_Kanal_Bot там будут выходить свежие новости,информация и различные обновления😊'''

    await bot.send_message(message.chat.id,text=text1)
    with open('video2.mp4', 'rb') as video_file:
        await bot.send_video(chat_id=message.chat.id, video=video_file)    
    text2 = '''ИНСТРУКЦИЯ №2 ❗️❗️❗️

Этапы, которые нужно сделать в этой инструкции:


1. Добавить созданную группу в созданную папку ( для удобства) 

2. Для того, чтобы бот работал - Нужно в строку ввести /start - После нажать на кнопку "Управление подпиской" - произвести оплату подписки и нажать на кнопку "Оплатил"✅

3. После оплаты можно вернуться в главное меню - нажать на кнопку "Проверить подписку💰" и убедиться, что подписка активна.

4. После успешной оплаты подписки можете переходить к пункту "Подключение аккаунта➕"'''
    
    await bot.send_message(message.chat.id,text=text2)
    with open('video3.mp4', 'rb') as video_file:
        await bot.send_video(chat_id=message.chat.id, video=video_file)    

    text3 = '''ИНСТРУКЦИЯ №3 ❗️❗️❗️

Этапы, которые нужно сделать в этой инструкции:


1. Переходим к пункту "Подключение аккаунта➕"

2. Вам нужно перейти к себе на авито в раздел "Для профессионалов" вкладка "Интеграции", снизу будет написано "Получить ключи" или они уже там будут

3. Копируйте слева "Номер профиля" он должен быть написан слитно БЕЗ ПРОБЕЛОВ❗️и вставляете в чат, который Вы создали

4. После копируйте ключи Client ID, Client secret. и вставляете это в чат который вы создали.

5. После того как вы скопировали ключи и номер профиля, нужно перейти в самого бота @SK2_Avito_bot ввести команду /start и нажать на кнопку "Список подключенных аккаунтов". Если вы увидите там свой аккаунт, значит вы сделали все ВЕРНО👍

PS. Инструкции по добавлению Автоответов пока что нет, но там никаких сложностей не должно возникнуть.

Больших продаж всем🚀 Будут вопросы обязательно пишите - Я всегда на связи🔥'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='💵 Проверить подписку',callback_data='check_vip'),types.InlineKeyboardButton(text='➕ Проверить подключеие ', callback_data='check_connection'))
    keyboard.add(types.InlineKeyboardButton(text='Проверить оплату',callback_data='check_money'))
    await bot.send_message(message.chat.id,text=text3,reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_vip')
async def check_vip(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    user_id = callback_query.message.chat.id
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли значение в атрибуте "тестовый период" для данного пользователя
    cursor.execute('SELECT test_period FROM chats WHERE chat_id = ?', (user_id,))
    test_period_end = cursor.fetchone()
    # Здесь предполагается, что вы извлекли дату и время окончания подписки из базы данных
    subscription_end_time = ''
    try:
        subscription_end_time = datetime.datetime.strptime(test_period_end[0], '%Y-%m-%d %H:%M:%S.%f')
    except Exception as e:
        print('Error:', e)
    
    if subscription_end_time is None:
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
        await bot.send_message(
            callback_query.message.chat.id,
            text='Ваша подписка истекла. Хотите продлить подписку?',
            reply_markup=keyboard,
        )
        # Здесь можете отправить клавиатуру с кнопкой для покупки подписки
    else:
        text = f"<b>У вас активная подписка до</b> {subscription_end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        sum = get_sum(tg_id=callback_query.message.chat.id)
        keyboard.add(types.InlineKeyboardButton(text='Продлить имеющуся подписку',url=sum))
        await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='html'
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'check_connection')
async def check_connection(callback_query: types.CallbackQuery):
    text = '''✋ Здравствуйте!


Пришлите номер профиля Avito.ru!


Номер профиля можете найти в личном кабинете слева, либо в меню "Профиль" в моб. приложении!

Client_id можно найти в разделе "Интеграции" по ссылке - https://www.avito.ru/professionals/api

Client_secret можно найти в разделе "Интеграции" по ссылке - https://www.avito.ru/professionals/api

❗️Важно: интегрировать сообщения можно только владельцам максимального / расширенного тарифов!

Шаблон:
49702411
LgF3nrObD3ftikUcqPRO
lgyY2nOjvsN9rcskeqkcEV9L2oDxQWtmqa78Qgig'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
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
    
    print("List of operations:")
    print("Next page starts with: ", history.next_record)
    
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
        
        # Обновите дату окончания подписки в базе данных
            update_subscription_end_date_in_database(callback_query.message.chat.id, one_month_later)
        
  
            
        # Здесь вы можете добавить логику для обновления атрибута test_period_end в базе данных
        # Например, получите текущее значение test_period_end из базы данных,
        # добавьте к нему месяц и обновите базу данных новым значением
        
        # Например (псевдокод):
        # current_test_period_end = get_test_period_end_from_database(callback_query.message.chat.id)
        # new_test_period_end = current_test_period_end + timedelta(days=30)
        # update_test_period_end_in_database(callback_query.message.chat.id, new_test_period_end)
        
    else:
        text += "У вас нет успешных оплат за последний месяц."
    
    # Создаем клавиатуру для возврата назад
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_chat_menu'))
    
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
    keyboard.add(types.InlineKeyboardButton(text='💵 Проверить подписку',callback_data='check_vip'),types.InlineKeyboardButton(text='➕ Проверить подключеие ', callback_data='check_connection'))
    keyboard.add(types.InlineKeyboardButton(text='Проверить оплату',callback_data='check_money'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'video')
async def video_sos(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    # Используйте callback_query.message.chat.id и callback_query.message.message_id
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='https://youtu.be/GUPi_qfCXbs',
        reply_markup=keyboard
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
        test_period_end = datetime.datetime.now() + datetime.timedelta(days=1)
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
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выдан тестовый доступ на 1 день.',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_wrapper')
async def back_wr(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='📹 Видеоинструкция',callback_data='video'),types.InlineKeyboardButton(text='➕ Подключение Avito',callback_data='req_avito'))
    keyboard.add(types.InlineKeyboardButton(text='🕥 Тестовый период',callback_data='test_period'),types.InlineKeyboardButton(text='📃 Автоотчеты',callback_data='auto_othcet'))
    keyboard.add(types.InlineKeyboardButton(text='🤖 Бот в чате',callback_data='vidoe'),types.InlineKeyboardButton(text='📤 Ответ на сообщение',callback_data='req_avito'))
    keyboard.add(types.InlineKeyboardButton(text='💾 Просмотр диалога',callback_data='vidoe'),types.InlineKeyboardButton(text='📑 Сценарии чатов',callback_data='req_avito'))
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад',callback_data='back_main'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'req_avito')
async def req_avito(callback_query: types.CallbackQuery):
    text = '''Подключение аккаунта Avito к боту
Один бот можно связать с неограниченным количеством аккаунтов.
Чтобы подключить аккаунт Avito, нажмите в меню 
«💰Управление подпиской» и следуйте инструкциям».'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад',callback_data='back_wrapper'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'auto_othcet')
async def auto_othcet(callback_query: types.CallbackQuery):
    text = '''Как работать с автоответами
Автоответы созданы для автоматического общения с клиентами. Есть 3 вида автоответов:

Второй пункт хорошо подходит компаниям, которые работают строго по графику. В "определенный промежуток времени" можете настроить текст для рабочего и нерабочего времени.

1. На первое сообщение. На этом этапе Вы можете запланировать неограченное количество приветственных сообщений подряд. Для этого нужно нажать на кнопку "На первое сообщение", далее ввести текст первого сообщения и нажать на Enter. Если нужен второй текст, то пишем второй текст. Если больше не нужно других текстов нажимаем кнопку "Пропустить". Выйдет системное сообщение "Автоовтеты добавлены" 
 
2. В определенный промежуток времени. Для этого нужно ввести для первого текста начальное и конечное время, затем ввести текст для первого автоответа, если нужно запланировать еще и второй автоответ, то вводим начальное и конечное время второго автоответа, затем сам текст. Если не нужен второй текст, тогда нажимаем кнопку "Пропустить".
Например: у Вас какая-то компания, Вы хотите, чтобы бот отвечал на сообщения клиентов в нерабочее время. Чтобы запланировать такую функцию, нужно нажать на кнопку "В определенный промежуток времени" после этого ввести начальное время по (МСК) "18:00" и затем конечное время "10:00" , далее нужно запланировать текст. 

3. На триггер. Бот будет отвечать, если увидит в сообщении клиента триггер, который вы назначили. Их может быть несколько для одного автоответа. Например: айфон, iphone, яблоко фон. И нет разницы, большие или маленькие буквы. Если бот увидит это слово или словосочетание в сообщении клиента, он сразу ответит ему заготовленным текстом. Если триггеров будет несколько в одном сообщении, бот отправит несколько сообщений. Вы можете эту функцию использовать для удобства и быстрого ответа клиенту. Или вовсе выстроить с ним диалог, выдавая варианты сообщений, которые нужно написать для получения той или иной информации.

Добавить автоответ
Чтобы создать автоответ, нажмите в меню кнопку «🤖Автоответы», далее «➕Добавить автоответ» и далее пошагово ответьте на сообщения бота.

Удалить автоответ
Чтобы удалить шаблон, нажмите в меню кнопку «🤖Автоответы», далее «👀Показать автоответы» и далее нажмите «Удалить» под ненужным шаблоном.

Вкл/Выкл
Чтобы включить или выключить автоответ нажмите на кнопку "вкл" или "выкл"

Редактировать автоответ
Для редактирования автоответа вам нужно нажать на кнопку "изменить" ввести заного время и сам текст.'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад',callback_data='back_wrapper'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'test_period')
async def test_period(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='back_wrapper'))

    # Отправляем изображения
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            with open(os.path.join(image_folder, filename), 'rb') as image_file:
                await callback_query.message.answer_photo(photo=image_file)

    text = '''Тестовый период
    Тестовый период дается на ровно 24 часа, для того чтобы Вы успели за это время протестировать все возможные функции. 

    После тестового периода, нужно оплатить бессрочную подписку. После оплаты сможете продолжить Вашу работу

    Что бы воспользоваться данной функцией нужно:
    1. Нажать в главном меню на кнопку "Тестовый период" (рис.1)
    2. После нажатия вас система оповестит о выданном тестовом периоде. (рис.2)
    3. В главном меню Вы можете нажать на кнопку "Проверить подписку" и посмотреть дату окончания тестового периода  (рис.3)
    4. Для продолжения работы после тестового периода, нужно оплатить бессрочную подписку.'''
    
    # Отправляем текст и клавиатуру
    await bot.send_message(callback_query.message.chat.id, text=text,reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'sos')
async def pomosh(callback_query: types.CallbackQuery):
    text = '''Выберите опцию'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='📃 Инструкция по использованию',callback_data='back_wrapper'),types.InlineKeyboardButton(text='📞 Связаться с поддержкой',callback_data='sos_with_me'))
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться в главное меню',callback_data='back_main'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'sos_with_me')
async def req_avito(callback_query: types.CallbackQuery):
    text = '''🤝 Поддержка команды
TiqAvito принимает сообщения 24 / 
‼️ Отвечаем ежедневно с 10:00 до 00:00. Иногда отвечаем в нерабочее время!

📤@Manager_Tiq_Shop📤'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться назад',callback_data='sos'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'auto_answera')
async def auto_answera(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Показать автоответы',callback_data='r'),types.InlineKeyboardButton(text='Добавить авоответ',callback_data='add_answer'))
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться в главное меню',callback_data='back_main'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Подтвердите',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_answer')
async def add_answer(callback_query: types.CallbackQuery):
    text = '''Выберите, в каком случае будем отправлять сообщение клиенту ⁉️ Будьте внимательны, автоответы будут применены для всех аккаунтов привязанных к боту. Если у вас несколько аккаунтов и вы вы хотите, чтобы в каждом аккаунте была своя логика. Создайте для каждого аккаунта отдельный чат в Telegram и добавьте туда бота для работы с сообщениями.'''
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='На первое сообщение',callback_data='first_message'),types.InlineKeyboardButton(text='В определенный промежуток времени',callback_data='time_message'))
    keyboard.add(types.InlineKeyboardButton(text='Триггеры',callback_data='triggers'))
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернуться в главное меню',callback_data='back_main'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard
    ) 

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_main')
async def back_main(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='📹Видеоинструкция',callback_data='video'),types.InlineKeyboardButton(text='📓Cписок подключенных аккаунтов',callback_data='spisok'))
    keyboard.add(types.InlineKeyboardButton(text='🤖Автоответы',callback_data='auto_answera'),types.InlineKeyboardButton(text='🆘Помощь',callback_data='sos'))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите опцию',
        reply_markup=keyboard
    ) 
@dp.message_handler(commands='unread')
async def unread_data(message: types.Message):
    global current_page2
    global current_page_message_id2
    # Define the number of contacts to display per page
    contacts_per_page = 6
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    # Clear the unique_user_names set for the current page
    unique_user_names.clear()
    user_id = get_user_id(message.chat.id)
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

@dp.message_handler(Command("data") & ChatTypeFilter(types.ChatType.GROUP))
async def get_data(message: types.Message, just = None):
    global current_page
    global current_page_message_id
    # Define the number of contacts to display per page
    contacts_per_page = 6
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    # Clear the unique_user_names set for the current page
    unique_user_names.clear()
    user_id = get_user_id(message.chat.id)
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
        if current_page_message_id and just==None:

            try:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=current_page_message_id,
                                            text="Выберите пользователя:", reply_markup=keyboard)
            except aiogram.utils.exceptions.MessageNotModified:
                # Если сообщение не было изменено, просто пропустите ошибку
                    # Если сообщение не было изменено, удаляем предыдущее сообщение и отправляем новое
                await bot.delete_message(chat_id=message.chat.id, message_id=current_page_message_id)
                message = await bot.send_message(chat_id=message.chat.id, text="Выберите пользователя:", reply_markup=keyboard)
                current_page_message_id = message.message_id
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
    # Trigger a refresh of the data
    await get_data(callback_query.message)




# # Обработчик коллбэков от кнопок
# @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('send_'))
# async def process_callback(callback_query: types.CallbackQuery):
#     user_name = callback_query.data.replace('send_', '')
#     await bot.send_message(callback_query.from_user.id, f"Вы выбрали пользователя: {user_name}")




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
    if len(action_data)>2:
        user_id, chat_id  = action_data[1], action_data[2]
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

    elif action == 'view-chat':
        # Обработка действия "Посмотреть чат"
        resp = get_user_id(callback_query.message.chat.id)  # Получаем client_id
        token = get_token(callback_query.message.chat.id)
        data = get_avito_messages(user_id=resp, chat_id=chat_id, token=token)
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
        user_id, chat_id = action_data[1], action_data[2]
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


@dp.message_handler(state=MyStates.waiting_for_text)
async def process_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        user_id = data['user_id']
        telegram_chat_id = data['telegram_chat_id']  # Получаем chat_id Telegram чата
        # Отправляем текстовое сообщение в чат с пользователем
        resp = get_user_id(message.chat.id)  # Получаем client_id
        token = get_token(message.chat.id)

        send_message(chat_id=chat_id, user_id=resp, text=message.text, token=token)
        mark_chat_as_read(resp, chat_id, token=token)
        
        # Отправляем уведомление о успешной отправке сообщения
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-message^{chat_id}^{user_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{chat_id}^{user_id}'))
        await bot.send_message(
            chat_id=telegram_chat_id,  # Используйте chat_id чата с пользователем
            text='Сообщение отправлено успешно!',
            parse_mode='html',
            reply_markup=keyboard
        )
    # Завершаем состояние
    await state.finish()



@dp.message_handler(content_types=types.ContentTypes.TEXT, chat_type=types.ChatType.GROUP)
async def check_pattern(message: types.Message):
    if message.text.startswith("Шаблон"):
        # Если сообщение начинается с "Шаблон", выполните нужные действия
        lst = message.text.split('\n')
        print(lst)
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        try:
            # Проверяем существование записи с указанным chat_id
            cursor.execute('SELECT id FROM chats WHERE chat_id = ?', (message.chat.id,))
            existing_chat = cursor.fetchone()
            print('exitsting_chat',existing_chat)
            if existing_chat != None:
                print('ggfgfgfg')
                cursor.execute('SELECT id, test_period FROM chats WHERE chat_id = ?', (message.chat.id,))
                time = cursor.fetchone()
                test_period_str = time[1]
                print(test_period_str)
                test_period_str = test_period_str.split('.')[0]  # Отбрасываем дробную часть секунды
                test_period = datetime.datetime.strptime(test_period_str, '%Y-%m-%d %H:%M:%S')
                if test_period <= datetime.datetime.now():
                    keyboard = types.InlineKeyboardMarkup()
                    sum = get_sum(tg_id=message.chat.id)
                    keyboard.add(types.InlineKeyboardButton(text='Продлить подписку',url=sum))
                    await message.reply(f"Ваш тестовый период истек. Для продолжения работы, пожалуйста оплатите подписку",reply_markup=keyboard)
                else:
                    token = set_personal_token(client_id=lst[2],client_secret=lst[3])
                    # Обновляем существующую запись в таблице chats
                    cursor.execute('UPDATE chats SET id_avito = ?, client_id = ?, client_secret = ?, token = ?  WHERE chat_id = ?',
                                (lst[1], lst[2], lst[3], token, message.chat.id))
                    conn.commit()
                    asyncio.create_task(background_task(message.chat.id))
            else:
                if test_period <= datetime.datetime.now():
                    keyboard = types.InlineKeyboardMarkup()
                    sum = get_sum(tg_id=message.chat.id)
                    keyboard.add(types.InlineKeyboardButton(text='Продлить подписку',url=sum))
                    await message.reply(f"Ваш тестовый период истек. Для продолжения работы, пожалуйста оплатите подписку",reply_markup=keyboard)
                else:
                    token = set_personal_token(client_id=lst[2],client_secret=lst[3])
                    # Если запись не существует, создаем новую
                    cursor.execute('INSERT INTO chats (chat_id, id_avito, client_id, client_secret,token) VALUES (?, ?, ?, ?, ?)',
                                (message.chat.id, lst[1], lst[2], lst[3], token))
                    
                    conn.commit()
                    asyncio.create_task(background_task(message.chat.id))
            
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
        keyboard.add(types.InlineKeyboardButton(text="🕸 Посмотореть ссылку для оплаты ", url='https://yoomoney.ru/transfer/quickpay?requestId=353339313234373332315f64636536343062613739396163313832353138336465376132343935653739633136313830646464'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'back_admin'))
        await bot.send_message(message.chat.id, 'Выберите опцию', reply_markup=keyboard)
    except Exception as e:
        print('Error:', str(e))

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('view_balance','chang_balance','view_site')))
async def action_callback(callback_query: types.CallbackQuery,state: FSMContext):
    if callback_query.data == 'view_balance':
        try:
                    # Получаем информацию из ЮMoney
            user = client.account_info()
            account_info = (
                f"Account number: <b>{user.account}</b>\n"
                f"Account balance: {user.balance} {user.currency}\n"
                f"Account status: {user.account_status}\n"
                f"Account type: {user.account_type}\n"
            )

            # Отправляем информацию в Telegram
            await callback_query.message.reply(account_info)

            # Отправляем информацию о связанных банковских картах
            cards = user.cards_linked
            if len(cards) != 0:
                card_info = "Information about linked bank cards:\n"
                for card in cards:
                    card_info += f"{card.pan_fragment} - {card.type}\n"
                await callback_query.message.reply(card_info,parse_mode='html')
            else:
                await callback_query.message.reply("No card is linked to the account")

        except Exception as e:
            await callback_query.message.reply(f"An error occurred: {str(e)}")
    elif callback_query.data == 'chang_balance':
        await bot.send_message(callback_query.from_user.id, "Введите текст сообщения:")

        # Устанавливаем состояние, чтобы ожидать ответа пользователя
        await YooMoneySum.waiting_fot_sum.set()



    else:
        pass

@dp.message_handler(state=YooMoneySum.waiting_fot_sum)
async def process_sum(message: Message, state: FSMContext):
    try:
        # Получаем введенную пользователем сумму
        user_input = message.text
        # Преобразуем введенный текст в число (проверьте, что это число)
        sum_to_set = float(user_input)

        # Изменяем сумму в Quickpay
        redirected_url = change_sum(sum_to_set)

        # Отправляем сообщение с новой суммой и ссылкой на оплату
        await message.answer(f"Сумма изменена на {sum_to_set} руб. Ссылка на оплату: {redirected_url}")

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
        await bot.send_message(message.chat.id,'Ты написал</>')

    # Здесь вы можете обрабатывать текстовые сообщения от пользователя
    # и выполнять соответствующие действия


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith(('view-chat-group^','send-message-group^')))
async def action_callback(callback_query: types.CallbackQuery,state: FSMContext):
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
        # Запрашиваем текст у пользователя
        await bot.send_message(callback_query.message.chat.id, "Введите текст сообщения:")

        # Устанавливаем состояние, чтобы ожидать ответа пользователя
        await MyStatesGroup.waiting_for_text.set()

        # Сохраняем chat_id и user_id в состоянии, чтобы использовать их в следующем шаге
        async with state.proxy() as data:
            data['chat_id'] = chat_id
            data['user_id'] = user_id
            data['telegram_chat_id'] = callback_query.message.chat.id  # Добавляем chat_id Telegram чата




    elif action == 'view-chat-group':
        # Обработка действия "Посмотреть чат"
        resp = get_user_id(callback_query.message.chat.id)  # Получаем client_id
        token = get_token(callback_query.message.chat.id)
        data = get_avito_messages(user_id=resp, chat_id=chat_id, token=token)
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

        mark_chat_as_read(resp, chat_id, token=token)
        # Отправляем объединенный текстовый чат
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message-group^{chat_id}^{user_id}'))
        await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=chat_text,
        parse_mode='html',
        reply_markup=keyboard
    )
        callback_query.data = f'send^{chat_id}^{user_id}'
    


@dp.message_handler(state=MyStatesGroup.waiting_for_text)
async def process_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data['chat_id']
        user_id = data['user_id']
        telegram_chat_id = data['telegram_chat_id']  # Получаем chat_id Telegram чата
        # Отправляем текстовое сообщение в чат с пользователем
        resp = get_user_id(message.chat.id)  # Получаем client_id
        token = get_token(message.chat.id)
        send_message(chat_id=chat_id, user_id=resp, text=message.text, token=token)
        mark_chat_as_read(resp, chat_id, token=token)
        print('мои данные',chat_id,user_id)
        # Отправляем уведомление о успешной отправке сообщения
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение еще раз", callback_data=f'send-message-group^{chat_id}^{user_id}'))
        keyboard.add(types.InlineKeyboardButton(text="🔚Назад", callback_data=f'seend^{chat_id}^{user_id}'))
        await bot.send_message(
            chat_id=telegram_chat_id,  # Используйте chat_id чата с пользователем
            text='Сообщение отправлено успешно!',
            parse_mode='html',
            reply_markup=keyboard
        )
    # Завершаем состояние
    await state.finish()

async def get_unread_messages(chat_id):
    avito_id = get_user_id(chat_id)
    token = get_token(chat_id)
    json_data = get_unread_messagef_avito(token=token, user_id=avito_id)
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
                f"Товар: {title} {price_string}\n"
                f"Автор товара: {client_name}\n"
                f"Город: {city}\n"
                f"Клиент: {author_name}\n\n"
                f"Текст сообщения:\n{last_message_text}\n\n"
                f"[Ссылка на товар]({url})"
            )
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="📨Отправить сообщение", callback_data=f'send-message-group^{avito_id}^{ch_id}'),types.InlineKeyboardButton(text="💬Посмотреть чат", callback_data=f'view-chat-group^{avito_id}^{ch_id}'))
                await bot.send_message(chat_id, text=response_message,parse_mode=types.ParseMode.MARKDOWN,reply_markup=keyboard)


async def background_task(chat_id):
    while True:
        print("Checking for unread messages...")
        # Получение всех непрочитанных сообщений
        await get_unread_messages(chat_id)
        await asyncio.sleep(5)  # Подождите 5 секунд перед повторным выполнением


if __name__ == '__main__':
    make_db()
    executor.start_polling(dp, skip_updates=True)