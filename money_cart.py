from yoomoney import Quickpay
import sqlite3


def change_sum(x):
    quickpay = Quickpay(
                receiver="4100117394518969",
                quickpay_form="shop",
                targets="Покупка на месяц Авито бота",
                paymentType="SB",
                sum=x,
                )
    print(quickpay.base_url)
    print(quickpay.redirected_url)
    return quickpay.redirected_url

def get_sum(tg_id):
    itog_summa = 1
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

        # Заданный id_telegram, для которого вы хотите получить client_id

        # SQL-запрос для выбора client_id по id_telegram
    cursor.execute("SELECT paysum,procent FROM payment")

        # Извлечение результата запроса
    result = cursor.fetchone()   
        # Шаг 2: Умножить procent на paysum
    cursor.execute("SELECT link_rel FROM chats WHERE chat_id = ?", (tg_id,))

# Извлечение результата запроса
    data = cursor.fetchone()
    if result:
        link_rel = data[0]
        paysum = result[0]
        procent = result[1]
        
        # Шаг 3: Получить всех пользователей, у которых who_linked содержит link_rel
        cursor.execute("SELECT COUNT(*) FROM chats WHERE who_linked LIKE ?", (f'%{link_rel}%',))
        num_linked_users = cursor.fetchone()[0]  # Получаем количество пользователей, у которых есть ваш link_rel

        # Шаг 4: Вычислить итоговую сумму
        itog_summa = paysum - ((paysum * (procent*num_linked_users))/100)
        
        print(itog_summa)
    else:
        itog_summa = result[0]  # Используйте здесь обычное значение

    print(result) 
    quickpay = Quickpay(
                receiver="4100117394518969",
                quickpay_form="shop",
                targets="Покупка на месяц Авито бота",
                paymentType="SB",
                sum=5,
                label=tg_id
                )
    return quickpay.redirected_url