# Автор данного скрипта - Максим (https://t.me/popov_web) // СКРИПТ ВЫЛАЖЕН В ОЗНАКОМИТЕЛЬНЫХ ЦЕЛЯХ И МОЖЕТ БЫТЬ ИСПОЛЬЗОВАТЬ В КАЧЕСТВЕ ОПЕН-СУРС РЕШЕНИЯ.
# Arzik bot v1.0 (https://t.me/kurarzikbot)

import telebot

API_TOKEN = 'токен бота'
ADMIN_ID = 'айди администратора'

bot = telebot.TeleBot(API_TOKEN)

user_questions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton('Задать вопрос')
    markup.add(btn)
    bot.send_message(message.chat.id, "Привет! Это бот для обратной связи с Арзиком :D", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Задать вопрос')
def ask_question(message):
    msg = bot.send_message(message.chat.id, 'Пришли текст своего вопроса, чтобы я смог ответить тебе на него.')
    bot.register_next_step_handler(msg, process_question)

def process_question(message):
    user_questions[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'Успех! Твой вопрос успешно отправлен, как только поступит ответ я обязательно тебе сообщу.')
    bot.send_message(ADMIN_ID, f"[REPORT SYSTEM]\n\nНовый вопрос от пользователя @{message.from_user.username}!\n\nТекст вопроса: {message.text}\n\n* Чтобы ответить на вопрос необходимо ввести /ask @{message.from_user.username} ответ")

@bot.message_handler(commands=['ask'])
def answer_question(message):
    try:
        command, username, *answer_text = message.text.split()
        answer_text = ' '.join(answer_text)
        chat_id = next(key for key, value in user_questions.items() if f'@{message.from_user.username}' == username)
        
        bot.send_message(chat_id, f"Поступил ответ от Арзика!\n\nСообщение: {answer_text}")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка. Убедитесь, что вы ввели команду правильно и пользователь существует.")

bot.polling(none_stop=True)
