import json
import settings
from storage import get_user_query, get_sudo_list, get_mod_list, get_request_query, get_order_query
from classes import Order, User, Delivery, Request
from datatypes import CallbackType, RequestType, OrderType, Location, OrderStatus
from datetime import datetime
from typing import Union


def delete_instance(instance, rtn_var=None):
    """A simple function that deletes the first arg and passes the other arg as a return value"""

    del instance
    return rtn_var


def create_user(chat_id: int, name: str) -> int:
    """A function for creating and saving a `User` object to database which takes `chat_id` and `name` as an argument"""

    user = User(cid=chat_id, name=name)

    return delete_instance(user, user.save())


def get_user(chat_id: int) -> Union[User, None]:
    """
    A function which attempts to get a user from the database using `chat_id`

    returns instance(User): if a user exists
    returns None: if a user doesn't exist
    """

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
        user = None

    return user


def user_exists(chat_id: int) -> bool:
    """
    A function which uses `get_user` to determine if a user exists or not

    returns True: if a user exists
    returns False: if a user doesn't exist
    """

    user = get_user(chat_id)

    return delete_instance(user, bool(user))


def user_enabled(chat_id: int) -> bool:
    """
    A function which takes `chat_id` as an argument and return a bool of the `user.enabled`

    returns True: if user.enabled
    returns False: if not user.enabled
    """

    user = get_user(chat_id)

    return delete_instance(user, user.enabled)


def get_sudo_cids() -> list:
    """
    A function which returns a list of sudo cids

    returns list[int]: if there are any sudos
    returns []: if there are no sudos
    """

    sudo_list = get_sudo_list()
    sudo_cids = []

    for sudo in sudo_list:
        sudo_cids.append(sudo['cid'])

    return sudo_cids


def get_callback_json(type: CallbackType, args: list) -> str:
    """
    A function which returns a dumped string dict object using the `type` and `args` arguments
    mostly used for inline_btn callback_data

    returns str
    """

    if type == CallbackType.sudo_mod:
        cid = args[0]
        status = args[1]

        query = {
            'type': CallbackType.sudo_mod,
            'cid': cid,
            'status': status,
        }

        return json.dumps(query).replace(' ', '')

    elif type == CallbackType.order_meal:
        cid = args[0]
        meal = args[1]

        query = {
            'type': CallbackType.order_meal,
            'cid': cid,
            'meal': meal,
        }

        return json.dumps(query).replace(' ', '')

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


def get_request(chat_id: int, type: RequestType) -> Request:
    """
    A function which takes `chat_id` and `type` as an argument and returns the specific request from the database

    returns instance(Request)
    """

    requestq = get_request_query(chat_id, type)

    request = Request(
        id=requestq.doc_id,
        type=requestq['type'],
        cid=requestq['cid'],
        mlist=requestq['mlist'],
    )

    return request


def create_request(type: RequestType, chat_id: int, mlist: list = []) -> int:
    """
    A function which takes `type`, `chat_id` and `mlist` as an argument and create a request and saves it to the database

    returns int
    """

    req = Request(type=type, cid=chat_id, mlist=mlist)

    return delete_instance(req, req.save())


def add_message_to_request(rcid: int, type: RequestType, mcid: int, mid: int) -> int:
    """
    A function which takes `rcid`, `type`, `mcid` and mid as an argument and adds a message to the mlist of the request and saves it to the database

    returns int
    """

    request = get_request(rcid, type)
    mcombo = [mcid, mid]

    request.mlist.append(mcombo)

    return delete_instance(request, request.update())


def get_request_mlist(chat_id: int, type: RequestType) -> list:
    """
    A function which takes `chat_id` and `type` as an argument and returns the mlist of the specific request

    returns list
    """

    request = get_request(chat_id, type)
    mlist = request.mlist

    return delete_instance(request, mlist)


def delete_request(chat_id: int, type: RequestType) -> int:
    """
    A function which takes `chat_id` and `type` as an argument and deletes the specific request from the database

    returns int
    """

    request = get_request(chat_id, type)

    return delete_instance(request, request.delete())


def request_exists(chat_id: int, type: RequestType):
    """
    A function which takes `chat_id` and `type` as an argument and returns a bool

    return True: if the request exists
    returns False: if the request doesn't exist
    """

    if get_request_query(chat_id, type):
        return True

    return False


def get_order(chat_id: str, meal: OrderType = None) -> Union[list, Order]:
    """
    A function which takes `chat_id` and `meal` as an argument and returns the specific order

    returns instance(Order): if order exists
    returns []: if order doesn't exist
    """

    userq = get_user_query(chat_id)
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


def create_order(uid: int = None, did: int = None, status: OrderStatus = None, meal: OrderType = None, location: Location = None, payment_mid: int = None, student_code: int = None, password: int = None, verification_code: int = None) -> int:
    """
    A function which takes `uid`, `did`, `status`, `meal`, `location`, `payment_mid`, `student_code`, `password` and `verification_code` as an argument and saves it to the database

    returns int
    """

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


def delete_order(chat_id: int, type: OrderType) -> int:
    """
    A function which takes `cid` and `type` as an argument and deletes the specific order from the database

    returns int
    """

    order = get_order(chat_id, type)

    return delete_instance(order, order.delete())


def get_location_type(loc: str) -> Location:
    """
    A function which takes `loc` as an argument which is a short location term and returns the `Location` value type of the specific location

    returns instance(Location)
    """

    if loc == 'uni':
        return Location.university

    elif loc == 'amin':
        return Location.aminian

    elif loc == 'rey':
        return Location.reyhane

    else:
        raise ValueError('Invalid Location')


def get_meals(chat_id: int) -> list[OrderType]:
    """
    A function which takes `chat_id` as an argument and checks available meals according to current time, and remove already ordered meals by the user from it and returns the list

    returns list[OrderType]
    """

    now = datetime.now(settings.TIMEZONE)

    meals = []
    meal_types = [OrderType.breakfast, OrderType.lunch, OrderType.dinner]

    breakfast_limit = now.replace(
        hour=settings.BREAKFAST_LIMIT['hour'], minute=settings.BREAKFAST_LIMIT['min'], second=0, microsecond=0)
    lunch_limit = now.replace(
        hour=settings.LUNCH_LIMIT['hour'], minute=30, second=0, microsecond=0)
    dinner_limit = now.replace(
        hour=settings.DINNER_LIMIT['hour'], minute=settings.DINNER_LIMIT['min'], second=0, microsecond=0)

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
