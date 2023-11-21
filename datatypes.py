class CallbackType:
    sudo_mod = 'sudo_mod'
    order_meal = 'o_meal'
    order_location = 'o_loc'


class CallbackStatus:
    request_not_found = 'request_not_found'


class RequestType:
    rank_req = 'rank_req'
    order_req = 'order_req'
    signup_req = 'signup_req'


class OrderType:
    breakfast = 'Breakfast'
    lunch = 'Lunch'
    dinner = 'Dinner'


class OrderStatus:
    created = 'created'
    meal_selected = 'meal_selected'
    location_selected = 'location_selected'
    scode_sent = 'scode_sent'
    password_sent = 'password_sent'
    confirmed = 'confirmed'
    accepted = 'accepted'
    declined = 'declined'
    delivered = 'delivered'
    canceled = 'canceled'


class Location:
    university = 'University'
    aminian = 'Aminian'
    reyhane = 'Reyhane'
