# Importing libraries
import telebot
from telebot import types
import openai
import schedule
import time
from epg_sraper import distribution_epg

# Installing the API key for openai
# forGitHUB_openai.api_key = 'TOKEN_CHAT_GPT'

# Creating a bot
# forGitHUB_TOKEN = 'TOKEN_BOT_FATHER'
# bot = telebot.TeleBot(TOKEN)

# Autorun of the parser, every 4 hours
games_epg = []


def games():
    global games_epg
    games_epg = distribution_epg()


games()


def job():
    schedule.every(4).hours.do(games)

    while True:
        schedule.run_pending()
        time.sleep(1)


# The function of sending EPG games
def epic_freebies(message):
    # Free distribution of EPG games
    bot.send_message(message.chat.id, "One second (¬‿¬)")
    bot.delete_message(message.chat.id, message.message_id + 1)
    if not games_epg:
        bot.send_message(message.chat.id, "Something goes wrong ¯\\_(ツ)_/¯")
    else:
        for game in games_epg:
            response = f"Name: {game['NAME']}\nStatus: {game['STATUS']}"
            bot.send_photo(message.chat.id, game['SRC'], caption=response)


# Handler for starting a dialog
def chat_gpt(message):
    gpt_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_markup = types.KeyboardButton("/stop")
    gpt_markup.add(stop_markup)
    bot.send_message(message.chat.id, "Ask any questions",
                     reply_markup=gpt_markup)
    bot.register_next_step_handler(message, chat_gpt_text)


# Initial instructions
system_content = "You are a very good, kind assistant. You are a telegram bot, so try to form an answer so that it is " \
                 "convenient to read. Your task is to help everyone with the questions that he/she will ask you to " \
                 "answer. You will be asked questions on: programming, physics, mathematics, chemistry, biology, " \
                 "social studies and many other sciences, as well as questions of the surrounding world, " \
                 "etc. Strictly prohibited: politics, religion, etc. You always answer in Russian and write any code " \
                 "in English, as is customary."

messages = [
    {"role": "system",
     "content": system_content,
     }
]


# Handler for text messages from the user
def chat_gpt_text(message):
    global messages
    text = message.text.lower()
    if text == "/stop":
        bot.send_message(message.chat.id, "All right, stop")

        # Clearing the message list and adding a system message
        messages = [
            {"role": "system",
             "content": system_content,
             }
        ]
        # Calling the function to end the dialog
        murk(message)
    else:
        try:
            content = message.text

            # Adding a user's message to the message list
            messages.append({"role": "user", "content": content})

            # Calling the GPT-3.5 API to generate a response
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            # Getting the generated response
            response = gpt_response.choices[0].message.content
            # Sending a response
            bot.send_message(message.chat.id, response)

            gpt_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            stop_markup = types.KeyboardButton("/stop")
            gpt_markup.add(stop_markup)
            bot.send_message(
                message.chat.id, "Ask any questions", reply_markup=gpt_markup)

            # Adding the bots response to message list
            messages.append({"role": "assistant", "content": response})

            # Continuation of the communication cycle
            bot.register_next_step_handler(message, chat_gpt_text)

        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id, "Something goes wrong ¯\\_(ツ)_/¯")


# Processing the start command
@bot.message_handler(commands=['start'])
def hello_world(message):
    bot.send_message(
        message.chat.id, "Hello, my friend (●'◡'●)", reply_markup=markup1)


markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_epg = types.KeyboardButton('Epic Freebies')
btn_gpt = types.KeyboardButton('Chat GPT')
markup1.add(btn_epg, btn_gpt)


def murk(message):
    bot.send_message(message.chat.id, "Something else?", reply_markup=markup1)


# Command Processing
@bot.message_handler(commands=['chatgpt'])
def for_gpt_command(message):
    chat_gpt(message)


# Command Processing
@bot.message_handler(commands=['epicstore'])
def for_epg_command(message):
    epic_freebies(message)


# Message processing
@bot.message_handler(func=lambda message: message.text.lower() == 'epic freebies')
def for_epg_text(message):
    epic_freebies(message)


# Message processing
@bot.message_handler(func=lambda message: message.text.lower() == 'chat gpt')
def for_gpt_command(message):
    chat_gpt(message)


# Command Processing
@bot.message_handler(commands=['stop'])
def for_stop_command(message):
    murk(message)


@bot.message_handler(commands=['info'])
def get_info(message):
    bot.send_message(message.chat.id, "WebScout - школьный проект, проверяющий собственные навыки программирования. "
                                      "Он умеет парсить раздачи с EPG store и отвечать на вопросы с помощью GPT-3.5.")


# Running the code
if __name__ == '__main__':
    bot.infinity_polling()
    job()
