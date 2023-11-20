import json
import settings
from storage import get_user_query, get_sudo_list, get_mod_list, get_request_query, get_order_query
from classes import Order, User, Delivery, Request
from datatypes import CallbackType, RequestType, OrderType, Location
from datetime import datetime

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
    if type == CallbackType.sudo_mod:
        cid = args[0]
        status = args[1]

        query = {
            'type': CallbackType.sudo_mod,
            'cid': cid,
            'status': status,
        }
        
        return json.dumps(query)

    elif type == CallbackType.order_meal:
        cid = args[0]
        meal = args[1]

        query = {
            'type': CallbackType.order_meal,
            'cid': cid,
            'meal': meal,
        }

        return json.dumps(query)

    elif type == CallbackType.order_location:
        cid = args[0]
        meal = args[1]
        location = args[2]

        query = {
            'type': CallbackType.order_location,
            'cid': cid,
            'meal': meal,
            'loc': location,
        }

        return json.dumps(query).replace(' ', '')


def get_mod_cids():
    pass


def get_request(cid, type):
    requestq = get_request_query(cid, type)

    request = Request(
        id=requestq.doc_id,
        type=requestq['type'],
        cid=requestq['cid'],
        mlist=requestq['mlist'],
    )

    return request

def create_request(type: RequestType, cid: int, mlist: list=[]):
    req = Request(type=type, cid=cid, mlist=mlist)

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


def get_order(cid, meal=None):
    userq = get_user_query(cid)
    uid = userq.doc_id
    orderq = get_order_query(uid, meal)

    if orderq:

        order = Order(
            id=orderq.doc_id,
            uid=orderq['uid'],
            did=orderq['did'],
            status=orderq['status'],
            meal=orderq['meal'],
            location=orderq['location'],
            payment_mid=orderq['payment_mid'],
            student_code=orderq['student_code'],
            password=orderq['password'],
            verification_code=orderq['verification_code'],
        )

        return order

    return []


def create_order(uid=None, did=None, status=None, meal=None, location=None, payment_mid=None, student_code=None, password=None, verification_code=None):
    order = Order(
        uid=uid,
        did=did,
        status=status,
        meal=meal,
        location=location,
        payment_mid=payment_mid,
        student_code=student_code,
        password=password,
        verification_code=verification_code,
    )

    return delete_instance(order, order.save())


def delete_order(cid, type):
    order = get_order(cid, type)

    return delete_instance(order, order.delete())


def get_location_type(loc):
    if loc == 'uni':
        return Location.university
    
    elif loc == 'amin':
        return Location.aminian
    
    elif loc == 'rey':
        return Location.reyhane
    
    else:
        raise ValueError('Invalid Location')


def get_meals(chat_id):
    now = datetime.now(settings.TIMEZONE)

    meals=[]
    meal_types = [OrderType.breakfast, OrderType.lunch, OrderType.dinner]

    breakfast_limit = now.replace(hour=settings.BREAKFAST_LIMIT['hour'], minute=settings.BREAKFAST_LIMIT['min'], second=0, microsecond=0)
    lunch_limit = now.replace(hour=settings.LUNCH_LIMIT['hour'], minute=30, second=0, microsecond=0)
    dinner_limit = now.replace(hour=settings.DINNER_LIMIT['hour'], minute=settings.DINNER_LIMIT['min'], second=0, microsecond=0)

    if now < breakfast_limit:
        meals.extend(OrderType.breakfast, OrderType.lunch, OrderType.dinner)
    
    elif breakfast_limit < now < lunch_limit:
        meals.extend(OrderType.lunch, OrderType.dinner)
    
    elif lunch_limit < now < dinner_limit:
        meals.append(OrderType.dinner)

    for meal in meal_types:
        exists = get_order(chat_id, meal)

        if exists:
            meals.remove(meal)
    
    return meals
