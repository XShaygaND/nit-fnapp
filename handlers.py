import settings
from tinydb import TinyDB, Query
from utils import get_user, user_exists, create_user, user_enabled, delete_instance, request_exists, create_request, delete_request, get_meals, create_order, get_order, delete_order, get_location_type
from classes import Order, User, Delivery
from datatypes import RequestType, OrderStatus, OrderType, CallbackType


def handle_user_status(chat_id, name):
    if not user_exists(chat_id):
        create_user(chat_id, name)
        return 1
    elif user_enabled(chat_id):
        return 0
    else:
        return -1


def handle_already_mod_sudo(chat_id):
    user = get_user(chat_id)

    already_requested = request_exists(chat_id, RequestType.rank_req)

    if not already_requested and not user.is_sudo and not user.is_mod:
        create_request(RequestType.rank_req, chat_id, [])

    return delete_instance(user, user.is_sudo or user.is_mod or already_requested)


def handle_sudo_code(chat_id, code, response):
    user = get_user(chat_id)

    if response == str(code):
        user.is_sudo = True
    else:
        handle_warn(user)

    delete_request(chat_id, RequestType.rank_req)
    user.update()

    return delete_instance(user, (user.is_sudo, user.warns, user.enabled))
        

def handle_new_mod_callback(query):
    cid = query['cid']
    status = query['status']
    user = get_user(cid)

    already_requested = request_exists(cid, RequestType.rank_req)

    if not already_requested:
        return delete_instance(user, (-1, user.warns))

    if status:
        user.is_mod = True
        user.update()
        
    else:
        handle_warn(user)
        user.update()
    
    delete_request(cid, RequestType.rank_req)

    return delete_instance(user, (user.is_mod, user.warns))


def handle_new_order_callback(query):
    type = query['type']
    cid = query['cid']
    meal = query['meal']

    already_requested = request_exists(cid, RequestType.order_req)

    if not already_requested:

        return delete_instance(order, -1)

    if type == CallbackType.order_meal:

        order = get_order(cid)
        available_meals = get_meals()
        
        if meal not in available_meals:
            delete_order(cid, meal)
            delete_request(cid, RequestType.order_req)

            return delete_instance(order, 0)
        
        else:
            order.status = OrderStatus.meal_selected
            order.meal = meal
            order.update()

            return delete_instance(order, 1)
    
    if type == CallbackType.order_location:
        location = query['loc']
        location = get_location_type(location)
        order = get_order(cid, meal)

        order.location = location
        order.status = OrderStatus.location_selected
        order.update()
        
        return delete_instance(order, 1)


def handle_new_order(chat_id):
    already_requested = request_exists(chat_id, RequestType.order_req)

    if already_requested:
        return -1
    
    user = get_user(chat_id)
    
    create_order(uid=user.id, status=OrderStatus.created)
    create_request(RequestType.order_req, chat_id)
    return get_meals()


def handle_student_code(chat_id, meal, student_code):
    order = get_order(chat_id, meal)
    already_requested = request_exists(chat_id, RequestType.order_req)

    if not already_requested:
        return delete_instance(order, -1)
    
    if not order.status == OrderStatus.location_selected:
        return delete_instance(order, -2)

    order.student_code = student_code
    order.status = OrderStatus.scode_sent
    order.update()

    return delete_instance(order, 1)


def handle_password(chat_id, meal, password):
    order = get_order(chat_id, meal)
    already_requested = request_exists(chat_id, RequestType.order_req)

    if not already_requested:
        return delete_instance(order, -1)
    
    if not order.status == OrderStatus.scode_sent:
        return delete_instance(order, -2)
    
    order.password = password
    order.status = OrderStatus.password_sent
    order.update()

    return delete_instance(order, 1)


def handle_warn(user: User):
    user.warns += 1

    if user.warns == settings.MAX_WARNS:
        user.enabled = False
    
    return
