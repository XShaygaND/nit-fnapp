import os
import dotenv
import json
import random
import settings
from telebot import TeleBot, types
from datatypes import CallbackType, RequestMessage
from utils import get_user, get_sudo_cids, get_callback_json, get_request_mlist, add_message_to_request
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


def delete_request_messages(mlist):
    for mcombo in mlist:
        bot.delete_message(mcombo[0], mcombo[1])


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
        msg = bot.send_message(sudo, 'New mod request:', reply_markup=markup)
        add_message_to_request(cid, RequestMessage.rank_req, msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    query = json.loads(call.data)
    type = query['type']

    if type == CallbackType.sudo_mod_req:

        cid = query['cid']
        mlist = get_request_mlist(cid, RequestMessage.rank_req)

        if mlist:
            delete_request_messages(mlist)
        status, warns = handle_new_mod_callback(query)


        if status == True:
            bot.send_message(cid, 'Your mod request has been accepted.')
        
        elif status == False:
            bot.send_message(cid, f"Your mod request has been rejected and you've been warned, Warns: {warns}/{settings.MAX_WARNS}")
            if warns == settings.MAX_WARNS:
                send_blocked_message(cid)

        return


@bot.message_handler(func=lambda message: True)
def check_user_status(message):
    cid = message.chat.id
    mid = message.message_id
    name = get_name(message)

    user_status = handle_user_status(cid, name)

    bot.delete_message(cid, mid)

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
    add_message_to_request(cid, RequestMessage.rank_req, cid, msg.message_id)

    bot.register_next_step_handler(msg, check_sudo_code, args=[code])


@bot.message_handler(func=not_mod_sudo, commands=['mod'])
def send_mod_request(message):
    cid = message.chat.id

    msg = bot.send_message(cid, 'Request sent to sudo.')
    add_message_to_request(cid, RequestMessage.rank_req, cid, msg.message_id)

    send_mod_to_sudos(message)


def check_sudo_code(message, args):
    cid = message.chat.id
    code = args[0]
    name = get_name(message)

    add_message_to_request(cid, RequestMessage.rank_req, cid, message.message_id)
    mlist = get_request_mlist(cid, RequestMessage.rank_req)
    delete_request_messages(mlist)

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
