from aiogram import Bot,Dispatcher,executor,types
import mysql.connector
from mysql.connector import Error
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class MyStates(StatesGroup):
    waiting_for_text = State()  # Состояние для ожидания текста от пользователя 


class TimeMessage(StatesGroup):
    waiting_for_text = State()  # Состояние для ожидания текста от пользователя 

class WorkTimeMessage(StatesGroup):
    waiting_for_text = State()


class SpecificTimeMessage(StatesGroup):
    waiting_for_text = State()  # Состояние для ожидания текста от пользователя 
    waiting_for_time = State()

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


# Создайте состояние для ожидания ввода заголовка
class TimeResponseStateTitle(StatesGroup):
    waiting_for_title = State()

# Создайте состояние для ожидания ввода ids
class TimeResponseStateIds(StatesGroup):
    waiting_for_ids = State()

# Создайте состояние для ожидания ввода текста
class TimeResponseStateText(StatesGroup):
    waiting_for_text = State()

# Создайте состояние для ожидания выбора даты
class TimeResponseStateWeekDays(StatesGroup):
    waiting_for_weekdays = State()

class TimeResponseStateStartTime(StatesGroup):
    waiting_for_start_time = State()

class TimeResponseStateEndTime(StatesGroup):
    waiting_for_end_time = State()

class AutoTriggers(StatesGroup):
    WaitingForTrigger = State()  # Ожидание ввода триггера
    WaitingForResponse = State()  # Ожидание ввода ответа



class YooMoneySum(StatesGroup):
    waiting_fot_sum = State()


class YooMoneyProcent(StatesGroup):
    waiting_fot_procent = State()


class ChangeAutoResponseStateTitle(StatesGroup):
    waiting_for_title = State()


class ChangeAutoResponseStateAnswer(StatesGroup):
    waiting_for_answer = State()

class ChangeAutoResponseStateWeekDaysChange(StatesGroup):
    waiting_for_weekdays_change = State()



class TimeChangeAutoResponseStateTitle(StatesGroup):
    waiting_for_title = State()


class TimeChangeAutoResponseStateAnswer(StatesGroup):
    waiting_for_answer = State()


class ChangeTimeResponseStateStartTime(StatesGroup):
    waiting_for_start_time = State()

class ChangeTimeResponseStateEndTime(StatesGroup):
    waiting_for_end_time = State()


class ChangeAutoTriggers(StatesGroup):
    WaitingForTrigger = State()  # Ожидание ввода триггера
    WaitingForResponse = State()  # Ожидание ввода ответа




class ChangeTimeResponseStateWeekDays(StatesGroup):
    waiting_for_weekdays = State()


class SetCode(StatesGroup):
    waiting_for_code= State()