import telebot
import data
from telebot import types
import types as pyTypes
import os

import symptoms

token = 'цыфарки:букавки'
#inDevBotToken = 'цыфарки:букавки'
#if os.getenv("INDEVTOKEN") == "1":
#    token = inDevBotToken
#    print("STARTING INDEV BOT")
bot = telebot.TeleBot(token)
userStates = dict()
userData1 = dict()


def install_keyboard(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in keyboard:
        item = types.KeyboardButton(i[0])
        markup.add(item)
    return markup


def install_keyboard2(keyboard):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in keyboard.keys():
        item = types.KeyboardButton(i)
        markup.add(item)
    return markup


def name_to_action(name):
    return data.states.get(name, data.actions)


def message_to_action(message: telebot.types.Message):
    chatId = message.chat.id
    if chatId not in userStates:
        userStates[chatId] = "actions"
        return data.actions
    return name_to_action(userStates[chatId])


def set_action(message: telebot.types.Message, action: str):
    userStates[message.chat.id] = action


@bot.message_handler(commands=['start'])
def button_message(message: telebot.types.Message):
    print(f"Got /start from {message.from_user.username}({message.chat.id} chat)")
    markup = install_keyboard(message_to_action(message))

    bot.send_message(message.chat.id, 'Привет, я бот помощник по аллергии и я готов помочь вам\n\n'
                                      'В случае проблем с кнопками введите /back', reply_markup=markup, )


@bot.message_handler(commands=['back'])
def button_message(message):
    print(f"Got /back from {message.from_user.username}({message.chat.id} chat)")

    set_action(message, "actions")
    markup = install_keyboard(message_to_action(message))

    bot.send_message(message.chat.id, 'Привет, всё исправлено!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message: telebot.types.Message):
    print(f"Got message! {message.text} from {message.from_user.username}({message.chat.id} chat) ")

    if userStates[message.chat.id] == "guess":
        add_guess(message)
        return

    action = message_to_action(message)
    markup = install_keyboard(action)
    found = False
    for option in action:
        if message.text == option[0]:
            if type(option[1]) == str:
                if option[1] == ">guess":
                    guess(bot, message)
                    return

                set_action(message, option[1])
                markup = install_keyboard(message_to_action(message))
                #bot.send_photo(message.chat.id, data.images["use_Buttons"], reply_markup=markup)
                bot.send_message(message.chat.id, "Воспользуйтесь кнопками", reply_markup=markup)
            elif type(option[1]) == pyTypes.FunctionType:
                option[1](bot, message)
            elif type(option[1]) == list:
                for i in option[1]:
                    if i.startswith("IMG@"):
                        bot.send_photo(message.chat.id, data.images[i.removeprefix("IMG@")], reply_markup=markup)
                    elif i.startswith("STEP@"):
                        set_action(message, i.removeprefix("STEP@"))
                        markup = install_keyboard(message_to_action(message))
                    else:
                        bot.send_message(message.chat.id, i, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Не известный тип', reply_markup=markup)
            found = True
            break
    if not found:
        bot.send_message(message.chat.id, 'Хм что-то не так! Воспользуйтесь кнопками или /back')


def guess(bot: telebot.TeleBot, message: telebot.types.Message):
    markup = install_keyboard2(symptoms.values)
    bot.send_message(message.chat.id, 'Выберите свои симптомы', reply_markup=markup)
    userData1[message.chat.id] = []
    set_action(message, "guess")


def add_guess(message: telebot.types.Message):
    markup = install_keyboard2(symptoms.values)

    if message.text == "далее >>":
        set_action(message, "actions")
        markup = install_keyboard(message_to_action(message))
        cur = symptoms.typesSet.copy()

        for i in userData1[message.chat.id]:
            if i in symptoms.values.keys():
                cur = cur.intersection(symptoms.values.get(i))

        if len(cur) > 0:
            q = 'Возможный типы аллергии:'

            for i in cur:
                q += "\n • " + i

            bot.send_photo(message.chat.id, data.images["guess_end"], q + "\nЭта информация может быть не точна. Для получения более точной информации "
                                              "обратитесь к врачу", reply_markup=markup)
        else:
            bot.send_photo(message.chat.id, data.images["guess_err"], "Мы не можем понять! Сходите к врачу", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '✅ | Добавлено в список', reply_markup=markup)
        userData1[message.chat.id].append(message.text)
        print(f"Added to userdata1 value: {message.text} for {message.from_user.username}({message.chat.id} chat)")


if __name__ == "__main__":
    bot.infinity_polling()
