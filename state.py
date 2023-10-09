from aiogram import Bot,Dispatcher,executor,types
import mysql.connector
from mysql.connector import Error
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class MyStates(StatesGroup):
    waiting_for_text = State()  # Состояние для ожидания текста от пользователя 

class MyStatesGroup(StatesGroup):
    waiting_for_text = State()  # Состояние для ожидания текста от пользователя 

# Создайте состояние для ожидания ввода заголовка
class AutoResponseStateTitle(StatesGroup):
    waiting_for_title = State()

# Создайте состояние для ожидания ввода ids
class AutoResponseStateIds(StatesGroup):
    waiting_for_ids = State()

# Создайте состояние для ожидания ввода текста
class AutoResponseStateText(StatesGroup):
    waiting_for_text = State()

# Создайте состояние для ожидания выбора даты
class AutoResponseStateWeekDays(StatesGroup):
    waiting_for_weekdays = State()

class AutoTriggers(StatesGroup):
    WaitingForTrigger = State()  # Ожидание ввода триггера
    WaitingForResponse = State()  # Ожидание ввода ответа



class YooMoneySum(StatesGroup):
    waiting_fot_sum = State()