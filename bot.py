import os
import dotenv
import json
import random
import settings
from telebot import TeleBot, types
from datatypes import CallbackType, RequestType, OrderStatus, Location
from utils import get_user, get_sudo_cids, get_callback_json, get_request_mlist, add_message_to_request, get_meals
from handlers import handle_user_status, handle_already_mod_sudo, handle_sudo_code, handle_new_mod_callback, handle_new_order, handle_new_order_callback, handle_student_code, handle_password
from telebot.handler_backends import ContinueHandling

dotenv.load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = TeleBot(token)

inline_btn = types.InlineKeyboardButton


def get_name(message: types.Message) -> str:
    """Takes a `Message` object and returns a user's `username` if they have one and their `first_name` if they don't"""

    chat = message.chat

    if chat.username:
        return chat.username
    return chat.first_name


def not_mod_sudo(message: types.Message) -> bool:
    """Takes a `Message` object and returns a bool indicating if the user is either mod or sudo"""

    cid = message.chat.id

    return not handle_already_mod_sudo(cid)


def send_blocked_message(chat_id: int) -> None:
    """Takes a cid and sends a message to the certain cid to notify them that their user is now disabled"""

    bot.send_message(
        chat_id, f'You have been blocked, for removal contact @Shaygan_2_2')
    # TODO: make it more advanced


def delete_request_messages(mlist: list[list]) -> None:
    """
    Takes a list of message lists and deletes each of them

    format: [[cid, mid], [cid, mid], ...]
    """

    for mcombo in mlist:
        bot.delete_message(mcombo[0], mcombo[1])


def send_mod_to_sudos(message: types.Message) -> None:
    """Takes a `Message` object and sends a mod request message to all the sudos which can be handled later"""

    sudos = get_sudo_cids()

    name = get_name(message)
    cid = message.chat.id

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    user_btn = inline_btn(text=name, url=f'tg://user?id={cid}')
    accept_btn = inline_btn(text='Accept', callback_data=get_callback_json(
        type=CallbackType.sudo_mod,
        args=[cid, True],
    ))
    decline_btn = inline_btn(text='Decline', callback_data=get_callback_json(
        type=CallbackType.sudo_mod,
        args=[cid, False],
    ))

    markup.row(user_btn).row(accept_btn, decline_btn)

    for sudo in sudos:
        msg = bot.send_message(sudo, 'New mod request:', reply_markup=markup)
        add_message_to_request(cid, RequestType.rank_req,
                               msg.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: types.CallbackQuery) -> None:
    """
    Base callback handler for inline_btn callbacks

    `CallbackType.sudo_mod`: Handles callbacks from mod inline_btn requests that were sent to sudos
    `CallbackType.order_meal`: Handles meal selection callbacks from series of meal inline_btns sent to user
    `CalblackType.order_location`: Handles location selection callbacks from series of location inline_btns sent to user
    """

    query = json.loads(call.data)
    type = query['type']

    if type == CallbackType.sudo_mod:

        cid = query['cid']
        mlist = get_request_mlist(cid, RequestType.rank_req)

        if mlist:
            delete_request_messages(mlist)

        status, warns = handle_new_mod_callback(query)

        if status == True:
            bot.send_message(cid, 'Your mod request has been accepted.')

        elif status == False:
            bot.send_message(
                cid, f"Your mod request has been rejected and you've been warned, Warns: {warns}/{settings.MAX_WARNS}")
            if warns == settings.MAX_WARNS:
                send_blocked_message(cid)

        return

    elif type == CallbackType.order_meal:

        cid = query['cid']
        meal = query['meal']

        status = handle_new_order_callback(query)

        if status in [-1, -2]:

            return

        elif status == 0:
            bot.send_message(cid, 'Meal is not available')

            return

        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1

        university = inline_btn(text=Location.university, callback_data=get_callback_json(
            type=CallbackType.order_location,
            args=[cid, meal, 'uni'],
        ))
        aminian = inline_btn(text=Location.aminian, callback_data=get_callback_json(
            type=CallbackType.order_location,
            args=[cid, meal, 'amin'],
        ))
        reyhane = inline_btn(text=Location.reyhane, callback_data=get_callback_json(
            type=CallbackType.order_location,
            args=[cid, meal, 'rey'],
        ))

        markup.add(university, aminian, reyhane)

        bot.edit_message_text(text='Select location:', chat_id=cid,
                              message_id=call.message.message_id, reply_markup=markup)

    elif type == CallbackType.order_location:
        cid = query['cid']
        meal = query['meal']

        status = handle_new_order_callback(query)

        if status:
            msg = bot.edit_message_text(
                "Student no.:", cid, call.message.message_id, reply_markup=None)

            bot.register_next_step_handler(msg, ask_password, args=[meal])


@bot.message_handler(func=lambda message: True)
def check_user_status(message: types.Message) -> None:
    """
    First message_handler of the bot to check if the user is enabled

    Deletes the message and continues handling it if the user is enabled
    Ignores the message and stops further handling if the user is disabled
    """

    cid = message.chat.id
    mid = message.message_id
    name = get_name(message)

    user_status = handle_user_status(cid, name)

    if user_status == 1:
        bot.send_message(cid, f'Welcome {name}')
    elif user_status == -1:
        return

    bot.delete_message(cid, mid)

    return ContinueHandling()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message) -> None:
    """Basic handler for the commands ('start', 'help') which sends a warm welcome"""

    cid = message.chat.id

    bot.send_message(cid, 'Welcome!')
    # TODO: Make more advanced


@bot.message_handler(func=not_mod_sudo, commands=['sudo'])
def ask_sudo_code(message: types.Message) -> None:
    """A handler for the command 'sudo' which generates a random 6 digit code and prints it in the console for the user to confirm"""

    cid = message.chat.id
    code = random.randint(100000, 999999)
    name = get_name(message)

    print(f'new sudo request from: {name}\ncode: {code}')

    msg = bot.send_message(cid, 'Enter sudo code:')
    add_message_to_request(cid, RequestType.rank_req, cid, msg.message_id)

    bot.register_next_step_handler(msg, check_sudo_code, args=[code])


@bot.message_handler(func=not_mod_sudo, commands=['mod'])
def send_mod_request(message: types.Message) -> None:
    """A handler for the command 'mod' which sends a mod request message to all sudos to be handled"""

    cid = message.chat.id

    msg = bot.send_message(cid, 'Request sent to sudo.')
    add_message_to_request(cid, RequestType.rank_req, cid, msg.message_id)

    send_mod_to_sudos(message)


@bot.message_handler(commands=['new'])
def ask_meal(message: types.Message) -> None:
    """A handler for the command 'new' which sends a message with a selection of meals to choose from"""

    cid = message.chat.id
    callback = handle_new_order(cid)

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1

    if callback == -1:
        return

    if callback:
        for meal in callback:
            meal_btn = inline_btn(text=meal, callback_data=get_callback_json(
                type=CallbackType.order_meal,
                args=[cid, meal],
            ))
            markup.add(meal_btn)

        msg = bot.send_message(cid, 'Available meals: ', reply_markup=markup)

        add_message_to_request(cid, RequestType.order_req, cid, msg.message_id)

    else:
        bot.send_message(cid, 'There are no available meals at this time.')


def check_sudo_code(message: types.Message, args: list) -> None:
    """A handler which checks the code send by the user and compares it to the sudo code in the console"""

    cid = message.chat.id
    code = args[0]
    name = get_name(message)

    add_message_to_request(cid, RequestType.rank_req, cid, message.message_id)
    mlist = get_request_mlist(cid, RequestType.rank_req)
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


def ask_password(message: types.Message, args: list) -> None:
    """A handler which verifies the Student no. sent by the user and asks for the password"""

    cid = message.chat.id
    mid = message.message_id
    student_code = message.text
    meal = args[0]

    bot.delete_message(cid, mid)

    if not student_code.isdigit():
        msg = bot.send_message(
            cid, 'Student no. can only consist of digits; Student code:')
        add_message_to_request(cid, RequestType.order_req, cid, msg.id)
        bot.register_next_step_handler(msg, ask_password, args=[meal])
        return

    status = handle_student_code(cid, meal, student_code)

    if status == 1:
        msg = bot.send_message(cid, 'Password:')
        add_message_to_request(cid, RequestType.order_req, cid, msg.id)
        bot.register_next_step_handler(msg, send_confirmation, args=[meal])


def send_confirmation(message: types.Message, args: list) -> None:
    """A handler which verifies the password sent by the user and sends a confirmation message to the user"""
    cid = message.chat.id
    mid = message.message_id
    password = message.text
    meal = args[0]

    bot.delete_message(cid, mid)

    if not password.isdigit():
        msg = bot.send_message(
            cid, 'Password can only consist of digits; Password:')
        add_message_to_request(cid, RequestType.order_req, cid, msg.id)
        bot.register_next_step_handler(msg, send_confirmation, args=[meal])
        return

    mlist = get_request_mlist(cid, RequestType.order_req)
    delete_request_messages(mlist)

    status = handle_password(cid, meal, password)

    if status == 1:
        bot.send_message(
            cid, 'Your order has been registered and is awaiting approval.')
        # TODO: Send request to mods


if __name__ == '__main__':
    bot.polling()
