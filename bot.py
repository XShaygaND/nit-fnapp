import os
import dotenv
import json
import random
import settings
from telebot import TeleBot, types
from datatypes import CallbackType
from utils import get_user, get_sudo_cids, get_callback_json
from handlers import handle_user_status, handle_already_mod_sudo, handle_sudo_code, handle_new_mod_callback
from telebot.handler_backends import ContinueHandling

dotenv.load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = TeleBot(token)

inline_keyboard_btn = types.InlineKeyboardButton


def get_name(message):
    chat = message.chat

    if chat.username:
        return chat.username
    return chat.first_name


def not_mod_sudo(message):
    cid = message.chat.id
    mid = message.message_id

    return not handle_already_mod_sudo(cid, mid)


def send_blocked_message(cid):
    bot.send_message(cid, f'You have been blocked, for removal contact @Shaygan_2_2')


def send_mod_to_sudos(message):
    sudos = get_sudo_cids()

    name = get_name(message)
    cid = message.chat.id

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    user_btn = inline_keyboard_btn(text=name, url=f'tg://user?id={cid}')
    accept_btn = inline_keyboard_btn(text='Accept', callback_data=get_callback_json(
        type=CallbackType.sudo_mod_req,
        args=[cid, True],
    ))
    decline_btn = inline_keyboard_btn(text='Decline', callback_data=get_callback_json(
        type=CallbackType.sudo_mod_req,
        args=[cid,False],
    ))

    markup.row(user_btn).row(accept_btn, decline_btn)

    for sudo in sudos:
        bot.send_message(sudo, 'New mod request:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    query = json.loads(call.data)
    type = query['type']

    if type == CallbackType.sudo_mod_req:

        cid = query['cid']
        status, warns = handle_new_mod_callback(query)

        if status == True:
            bot.send_message(cid, 'Your mod request has been accepted.')
            return
        
        bot.send_message(cid, f"Your mod request has been rejected and you've been warned, Warns: {warns}/{settings.MAX_WARNS}")
        if warns == settings.MAX_WARNS:
            send_blocked_message(cid)


@bot.message_handler(func=lambda message: True)
def check_user_status(message):
    cid = message.chat.id
    name = get_name(message)

    user_status = handle_user_status(cid, name)

    if user_status == 1:
        bot.send_message(cid, f'Welcome {name}')
    elif user_status == -1:
        return

    return ContinueHandling()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    cid = message.chat.id

    bot.send_message(cid, 'Welcome!')


@bot.message_handler(func=not_mod_sudo, commands=['sudo'])
def ask_sudo_code(message):

    cid = message.chat.id
    code = random.randint(100000, 999999)
    name = get_name(message)

    print(f'new sudo request from: {name}\ncode: {code}')

    msg = bot.send_message(cid, 'Enter sudo code:')
    bot.register_next_step_handler(msg, check_sudo_code, args=[code])


@bot.message_handler(func=not_mod_sudo, commands=['mod'])
def send_mod_request(message):
    cid = message.chat.id
    name = get_name(message)

    bot.send_message(cid, 'Request sent to sudo.')
    send_mod_to_sudos(message)


def check_sudo_code(message, args):
    cid = message.chat.id
    code = args[0]
    name = get_name(message)

    sudo, warns, enabled = handle_sudo_code(cid, code, message.text)

    if sudo:
        print(f'sudo set for user: {name}')
        bot.send_message(cid, "Sudo set.")
    else:
        print(
            f'failed sudo attempt by user: {name}, Warns: {warns}/{settings.MAX_WARNS}')
        bot.send_message(
            cid, f'Wrong code, Warns: {warns}/{settings.MAX_WARNS}')

    if not enabled:
        send_blocked_message(cid)


if __name__ == '__main__':
    bot.polling()
