import schedule
import time
import sqlite3
from datetime import datetime, date


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def job():
    print("Работаю")

    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Birthdays')
    results = cursor.fetchall()

    for person in results:
        d = datetime.strptime(person[2], '%d.%m.%Y')
        age = calculate_age(d)
        friend = person[2].split('.')
        b_day = datetime.strptime(f'{friend[0]}-{friend[1]}-{int(friend[2]) + age + 1}', '%d-%m-%Y').date()
        today = datetime.today().date()

        period = b_day - today

        if 2 <= period.days < 3:
            print(f"Не забудь поздравить {person} с днём рождения, он уже через 2 дня! Исполнится {age+1}")
            
        elif 1 <= period.days < 2:
            print(f"Не забудь поздравить {person} с днём рождения, он уже завтра! Исполнится {age+1}")
            
        elif period.days >= 365:
            print(f"Не забудь сегодня поздравить {person} с днём рождения! Исполнилось {age}")
            
        else:
            # print("В ближайшее время никаких дней рождения не предвидется")
            pass
            

# schedule.every().day.at("10:30").do(job)
# schedule.every(10).minutes.do(job)
schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)