import settings
from tinydb import TinyDB, Query
from utils import get_user, user_exists, create_user, user_enabled, delete_instance, request_exists, create_request, delete_request
from classes import Order, User, Delivery
from datatypes import RequestMessage


def handle_user_status(chat_id, name):
    if not user_exists(chat_id):
        create_user(chat_id, name)
        return 1
    elif user_enabled(chat_id):
        return 0
    else:
        return -1


def handle_already_mod_sudo(chat_id, message_id):
    user = get_user(chat_id)

    already_requested = request_exists(chat_id, RequestMessage.rank_req)

    if not already_requested and not user.is_sudo and not user.is_mod:
        create_request(RequestMessage.rank_req, chat_id, message_id)

    return delete_instance(user, user.is_sudo or user.is_mod or already_requested)


def handle_sudo_code(chat_id, code, response):
    user = get_user(chat_id)

    if response == str(code):
        user.is_sudo = True
    else:
        handle_warn(user)

    delete_request(chat_id, RequestMessage.rank_req)
    user.update()

    return delete_instance(user, (user.is_sudo, user.warns, user.enabled))
        

def handle_new_mod_callback(query):
    cid = query['cid']
    status = query['status']
    user = get_user(cid)

    if status:
        user.is_mod = True
        user.update()
        
    else:
        handle_warn(user)
        user.update()
    
    delete_request(cid, RequestMessage.rank_req)

    return delete_instance(user, (user.is_mod, user.warns))



def handle_warn(user: User):
    user.warns += 1

    if user.warns == settings.MAX_WARNS:
        user.enabled = False
    
    return
