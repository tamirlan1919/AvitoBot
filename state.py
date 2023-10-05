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


class AutoResponseState(StatesGroup):
    WaitingForTitle = State()  # Состояние ожидания ввода заголовка
    WaitingForAvitoIds = State()  # Состояние ожидания ввода ids объявления
    WaitingForResponseText = State()  # Состояние ожидания ввода текста сообщения
    WaitingForWeekDays = State()
    WaitingForConfirmation = State()  # Состояние ожидания подтверждения


class AutoTriggers(StatesGroup):
    WaitingForTrigger = State()  # Ожидание ввода триггера
    WaitingForResponse = State()  # Ожидание ввода ответа



class YooMoneySum(StatesGroup):
    waiting_fot_sum = State()