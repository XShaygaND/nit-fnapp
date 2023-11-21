from tinydb import TinyDB, Query

image_dir = 'images/'

db = TinyDB('db.json')
users = db.table('users')
orders = db.table('orders')
requests = db.table('requests')


def save_user(cid: int, name: str, enabled: bool, order_count: int, warns:int, is_sudo: bool, is_mod: bool) -> int:
    """
    A function which saves the user according to the args provided to the database

    returns int
    """
    
    query = {
        'cid': cid,
        'name': name,
        'enabled': enabled,
        'order_count': order_count,
        'warns': warns,
        'is_sudo': is_sudo,
        'is_mod': is_mod,
    }

    return users.insert(query)


def update_user(id: int, cid: int, name: str, enabled: bool, order_count: int, warns:int, is_sudo: bool, is_mod: bool) -> int:
    """
    A function which updates the user according to the args provided to the database

    returns int
    """
    
    query = {
        'cid': cid,
        'name': name,
        'enabled': enabled,
        'order_count': order_count,
        'warns': warns,
        'is_sudo': is_sudo,
        'is_mod': is_mod,
    }

    users.update(query, doc_ids=[id])


def get_user_query(chat_id: int):
    """
    A function which takes `chat_id` as an argument and searches the database for the specific user and returns it

    returns Document: if the user exists
    returns None: if the user doesn't exist
    """
    
    UserQ = Query()
    userq = users.get(UserQ.cid == chat_id)

    return userq


def get_sudo_list():
    UserQ = Query()
    sudo_usersq = users.search(UserQ.is_sudo==True)

    return sudo_usersq


def save_order(uid: int, did: int, status: str, meal: str, location: str, payment_mid: int, student_code: int, password: int, verification_code: int) -> int:
    """
    A function which saves the order according to the args provided to the database

    returns int
    """
    
    query = {
        'uid': uid,
        'did': did,
        'status': status,
        'meal': meal,
        'location': location,
        'payment_mid': payment_mid,
        'student_code': student_code,
        'password': password,
        'verification_code': verification_code,
    }

    return orders.insert(query)


def update_order(id: int, uid: int, did: int, status: str, meal: str, location: str, payment_mid: int, student_code: int, password: int, verification_code: int) -> int:
    """
    A function which updates the order according to the args provided in the database

    returns int
    """
    
    query = {
        'uid': uid,
        'did': did,
        'status': status,
        'meal': meal,
        'location': location,
        'payment_mid': payment_mid,
        'student_code': student_code,
        'password': password,
        'verification_code': verification_code,
    }

    return orders.update(query, doc_ids=[id])


def delete_order(cid:int, type:str) -> int:
    """
    A function which takes `cid` and `type` as arguments and deletes the order with the specific arguments from the database

    returns int
    """
    
    Order = Query()
    return orders.remove(cond=(Order.cid==cid) & (Order.meal==type))


def get_order_query(uid, meal=None):
    """
    A function which takes `uid` and `meal` as an argument and searches the database for the specific order and returns it

    returns Document: if the order exists
    returns None: if the order doesn't exist
    """
    Order = Query()
    orderq = orders.get(cond=(Order.uid==uid) & (Order.meal==meal))
    
    return orderq


def save_image(file, filename):
    with open(f'{image_dir}{filename}.png', 'wb') as new_file:
        new_file.write(file)


def get_mod_list_query() -> list:
    """
    A function which returns a list[Document] of the users that have the attribute `is_mod==True`

    returns list[Document]: if there are any mods
    returns None: if there aren't any mods
    """
    
    UserQ = Query()
    mod_usersq = users.search(UserQ.is_mod==True)

    return mod_usersq

def save_request(type: str, cid: int, mlist: list[list]) -> int:
    """
    A function which saves the request according to the arguments provided to the database

    returns int
    """
    
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
    }

    requests.insert(query)


def update_request(id: int, type: str, cid: int, mlist: list[list]):
    """
    A function which updates the request according to the arguments provided in the database

    returns int
    """
    
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
    }

    requests.update(query, doc_ids=[id])

def delete_request(cid:int, type:str) -> int:
    """
    A function which takes `cid` and `type` as an argument and deletes the specific request from the database

    returns int
    """
    
    Request = Query()
    return requests.remove(cond=(Request.cid==cid) & (Request.type==type))

def get_request_query(cid:int, type:str):
    """
    A function which takes `cid` and `type` as an argument and searches the database for the specific request and returns it

    returns Document: if the request exists
    returns None: if the request doesn't exist
    """
    
    Request = Query()
    requestq =  requests.get(cond=(Request.cid==cid) & (Request.type==type))

    return requestq


def get_orders():
    """
    A function which returns all the orders in the database

    returns list[Document]: if there are any orders
    returns None: if there are no orders
    """
    return orders.all()
