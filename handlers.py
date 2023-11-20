import settings
from tinydb import TinyDB, Query
from utils import get_user, user_exists, create_user, user_enabled, delete_instance, request_exists, create_request, delete_request, get_meals, create_order, get_order, delete_order, get_location_type
from classes import Order, User, Delivery
from datatypes import RequestType, OrderStatus, OrderType, CallbackType
from typing import Union


def handle_user_status(chat_id: int, name: str) -> int:
    """
    A handler for handling the user status

    returns 1: if a user doesn't exist
    returns 0: if the user is enabled
    returns -1: if the user is disabled
    """

    if not user_exists(chat_id):
        create_user(chat_id, name)
        return 1
    elif user_enabled(chat_id):
        return 0
    else:
        return -1


def handle_already_mod_sudo(chat_id: int) -> bool:
    """
    A handler which checks if the user is a mod or a sudo

    returns True: if the user is a mod, is a sudo, or has already requested for either
    returns False: if the user isn't a mod, isn't a sudo, and hasn't requested for either
    """

    user = get_user(chat_id)

    already_requested = request_exists(chat_id, RequestType.rank_req)

    if not already_requested and not user.is_sudo and not user.is_mod:
        create_request(RequestType.rank_req, chat_id, [])

    return delete_instance(user, user.is_sudo or user.is_mod or already_requested)


def handle_sudo_code(chat_id: int, code: int, response: Union[int, str]) -> tuple:
    """
    A handler which compares the generated code with the user response
    sets `user.is_sudo` to `True` if the code matches and warns the user otherwise

    returns (user.is_sudo, user.warns, user.enabled)
    """

    user = get_user(chat_id)

    if response == str(code):
        user.is_sudo = True
    else:
        handle_warn(user)

    delete_request(chat_id, RequestType.rank_req)
    user.update()

    return delete_instance(user, (user.is_sudo, user.warns, user.enabled))


def handle_new_mod_callback(query: dict) -> Union[int, tuple]:
    """
    A handler which handles callbacks from mod request messages sent to sudos

    returns -1: if the request no longer exists
    returns (user.is_mod, user.warns) otherwise
    """

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


def handle_new_order_callback(query: dict) -> int:
    """
    A handler which handles callback from the 'new' command

    if callback type is of `order_meal`:
        returns 0 if the meal is not in available meals
        returns 1 otherwise

    if callback type is of `order_location`:
        returns 1
    """

    type = query['type']
    cid = query['cid']
    meal = query['meal']

    already_requested = request_exists(cid, RequestType.order_req)

    if not already_requested:

        return delete_instance(order, -1)

    if type == CallbackType.order_meal:

        order = get_order(cid)
        available_meals = get_meals(cid)

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


def handle_new_order(chat_id: int) -> Union[int, list, None]:
    """
    A handler which handles calls from the 'new' command

    return 1: if the user has already created an order request
    returns meals: if there are meals available and no request exists
    returns None: otherwise
    """

    already_requested = request_exists(chat_id, RequestType.order_req)

    if already_requested:
        return -1

    meals = get_meals(chat_id)

    user = get_user(chat_id)

    if meals:
        create_order(uid=user.id, status=OrderStatus.created)
        create_request(RequestType.order_req, chat_id)

        return meals


def handle_student_code(chat_id: int, meal: OrderType, student_code: Union[int, str]) -> int:
    """
    A handler which handles the `student_code` sent by the user

    returns -1: if the request no longer exists
    returns -2: if order status isn't `location_selected`
    returns 1: otherwise
    """

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


def handle_password(chat_id: int, meal: OrderType, password: Union[int, str]) -> int:
    """
    A handler which handles the `passwowrd` sent by the user

    returns -1: if the request no longer exists
    returns -2: if the order status isn't `scode_sent`
    returns 1: otherwise
    """

    order = get_order(chat_id, meal)
    already_requested = request_exists(chat_id, RequestType.order_req)

    if not already_requested:
        return delete_instance(order, -1)

    if not order.status == OrderStatus.scode_sent:
        return delete_instance(order, -2)

    order.password = password
    order.status = OrderStatus.password_sent
    order.update()

    delete_request(chat_id, RequestType.order_req)

    return delete_instance(order, 1)


def handle_warn(user: User) -> None:
    """
    A handler which handles warning users

    returns None
    """

    user.warns += 1

    if user.warns == settings.MAX_WARNS:
        user.enabled = False

    return
