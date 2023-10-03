import schedule
import time
def job():
    print("Checking for unread messages...")

# Запускаем задачу каждую минуту
schedule.every(5).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)