from aiogram import Bot,Dispatcher,executor,types
import mysql.connector
from mysql.connector import Error
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class MyStates(StatesGroup):
    waiting_for_text = State()  # Состояние для ожидания текста от пользователя 


class YooMoneySum(StatesGroup):
    waiting_fot_sum = State()