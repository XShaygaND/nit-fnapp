import json
from storage import get_user_query, get_sudo_list, get_mod_list, get_request_query
from classes import Order, User, Delivery, Request
from datatypes import CallbackType, RequestMessage

def delete_instance(instance, rtn_var=None):
    del instance
    return rtn_var


def create_user(chat_id, name):
    user = User(cid=chat_id, name=name)

    return delete_instance(user, user.save())


def get_user(chat_id):
    userq = get_user_query(chat_id)

    if userq:
        user = User(
            id=userq.doc_id,
            cid=userq['cid'],
            name=userq['name'],
            enabled=userq['enabled'],
            order_count=userq['order_count'],
            warns=userq['warns'],
            is_sudo=userq['is_sudo'],
            is_mod=userq['is_mod'],
        )
    else:
        user = False

    return user


def user_exists(chat_id):
    user = get_user(chat_id)

    return delete_instance(user, bool(user))


def user_enabled(chat_id):
    user = get_user(chat_id)

    return delete_instance(user, user.enabled)


def get_sudo_cids():
    sudo_list = get_sudo_list()
    sudo_cids = []

    for sudo in sudo_list:
        sudo_cids.append(sudo['cid'])

    return sudo_cids


def get_callback_json(type: CallbackType, args):
    if type == CallbackType.sudo_mod_req:
        cid = args[0]
        status = args[1]

        query = {
            'type': CallbackType.sudo_mod_req,
            'cid': cid,
            'status': status
        }
        
        return json.dumps(query)


def get_mod_cids():
    pass


def get_request(cid, type):
    requestq = get_request_query(cid, type)

    request = Request(
        id=requestq.doc_id,
        type=requestq['type'],
        cid=requestq['cid'],
        mid=requestq['mid'],
        mlist=requestq['mlist'],
    )

    return request

def create_request(type: RequestMessage, cid: int, mid: int, mlist: list=[]):
    req = Request(type=type, cid=cid, mid=mid, mlist=mlist)

    return delete_instance(req, req.save())


def add_message_to_request(rcid, type, mcid, mid):
    request = get_request(rcid, type)
    mcombo = [mcid, mid]

    request.mlist.append(mcombo)

    return delete_instance(request, request.update())


def get_request_mlist(cid, type):
    request = get_request(cid, type)
    mlist = request.mlist

    return delete_instance(request, mlist)


def delete_request(cid, type):
    request = get_request(cid, type)

    return delete_instance(request, request.delete())

def request_exists(cid, type):
    if get_request_query(cid, type):
        return True
    
    return False
