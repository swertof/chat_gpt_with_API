from chatgpt_API import api_key
from telebot_api import *
import openai

import telebot
from telebot import types

i=0
bot = telebot.TeleBot(telebot_api)
openai.api_key = api_key[i]

@bot.message_handler(content_types=['text'])
#Ответ на первое сообщение
def start_message(message):
    hi_mess=bot.send_message(message.chat.id,"Привет, это телеграмм бот для общения с ИИ! Задавай вопросы.")
    bot.register_next_step_handler(hi_mess,chating)
def chating(message):
    user_input=message.text
    # Отправка запроса к API GPT-3
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Выбор модели GPT-3
            messages=[{"role": "user", "content": user_input}],
        )
        #Ответ пользователю
        user_output=bot.send_message(message.chat.id,(response.choices[0]['message']['content']))
    
    # Исключение, если API перестает отвечать
    except openai.error.AuthenticationError:
        global i
        if i+1 >= len(api_key):
            user_output=bot.send_message(message.chat.id,"Я сломался абсолютно точно 😢. Подождите, может быть меня скоро починят.")
        else:
            i+=1
            openai.api_key = api_key[i]
            user_output=bot.send_message(message.chat.id,"Кажется я сломался 😰! Попробуй написать снова, вдруг я заработаю.")
    bot.register_next_step_handler(user_output,chating)
if __name__=="__main__":
    bot.infinity_polling()

