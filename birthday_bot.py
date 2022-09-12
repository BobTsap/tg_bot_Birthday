from datetime import date
import telebot
import sqlite3
from my_token import my_token


# Работает добавление и удаление записи в БД!
# Теперь написать сами оповещения, обработку даты

# Улучшения: формат даты, выбор кого удалить из повторных, кнопка печати ближайших 10 ДР

bot = telebot.TeleBot(my_token)

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_name: str, birthday: date):
	cursor.execute('INSERT INTO Birthdays (user_name, birthday) VALUES (?, ?)', (user_name, birthday))
	conn.commit()

name_for_birthday = ''
date_birthday = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Добавить', 'Удалить')
    bot.send_message(message.chat.id, 'Привет! Хочешь добавить или удалить новую запись?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Добавить':
        bot.send_message(message.from_user.id, 'Введите имя для добавления')
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'Удалить':
        bot.send_message(message.from_user.id, 'Введите имя для удаления')
        bot.register_next_step_handler(message, delete_name)

@bot.message_handler(content_types=['text'])
def delete_name(message):
    deleted_name = message.text
    cursor.execute(f'SELECT * FROM Birthdays WHERE user_name = "{deleted_name}" ORDER BY id')
    results = cursor.fetchall()
    conn.commit()
    if len(results) > 1:
        bot.send_message(message.from_user.id, 'В списке есть совпадения имен. \nНапишите номер (id) записи, которую следует удалить')
        for i in results:
            bot.send_message(message.from_user.id, f'id={i[0]}: {i[1]}, {i[2]} г.р.')
        bot.register_next_step_handler(message, get_id)



    elif len(results) == 1:
        bot.send_message(message.from_user.id, f'Запись: {results[0][1]}, {results[0][2]} удалена из напоминаний')
        cursor.execute(f'DELETE FROM Birthdays WHERE id = "{results[0][0]}"')
        conn.commit()


@bot.message_handler(content_types=['text'])
def get_id(message):
    id_for_del = message.text
    cursor.execute(f'SELECT * FROM Birthdays WHERE id = "{id_for_del}"')
    result = cursor.fetchall()
    conn.commit()
    bot.send_message(message.from_user.id, f'Запись: {result[0][1]}, {result[0][2]} удалена из напоминаний')
    cursor.execute(f'DELETE FROM Birthdays WHERE id = "{message.text}"')
    conn.commit()


def get_name(message):
    global name_for_birthday
    name_for_birthday = message.text
    bot.send_message(message.from_user.id, 'Введите дату в формате дд.мм.гггг')
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    global date_birthday
    date_birthday = message.text
    db_table_val(name_for_birthday, date_birthday)
    bot.send_message(message.from_user.id, 'Данные внесены!')
    bot.send_message(message.from_user.id, f'Теперь будут приходить напоминания о ДР: {name_for_birthday} {date_birthday}')
    
bot.polling(none_stop=True, interval=0)