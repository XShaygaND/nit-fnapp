from tinydb import TinyDB, Query

image_dir = 'images/'

db = TinyDB('db.json')
users = db.table('users')
orders = db.table('orders')
requests = db.table('requests')


def save_user(cid: int, name: str, enabled: bool, order_count: int, warns:int, is_sudo: bool, is_mod: bool):
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


def update_user(id: int, cid: int, name: str, enabled: bool, order_count: int, warns:int, is_sudo: bool, is_mod: bool):
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


def get_user_query(chat_id):
    UserQ = Query()
    userq = users.get(UserQ.cid == chat_id)

    return userq


def get_sudo_list():
    UserQ = Query()
    sudo_usersq = users.search(UserQ.is_sudo==True)

    return sudo_usersq


def save_order(uid, did, status, meal, location, payment_mid, student_code, password, verification_code):
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


def update_order(id, uid, did, status, meal, location, payment_mid, student_code, password, verification_code):
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


def delete_order(cid, type):
    Order = Query()
    return orders.remove(cond=(Order.cid==cid) & (Order.meal==type))


def get_order_query(uid, meal=None):
    Order = Query()
    orderq = orders.get(cond=(Order.uid==uid) & (Order.meal==meal))
    
    return orderq


def save_image(file, filename):
    with open(f'{image_dir}{filename}.png', 'wb') as new_file:
        new_file.write(file)


def get_mod_list():
    UserQ = Query()
    mod_usersq = users.search(UserQ.is_mod==True)

    return mod_usersq

def save_request(type, cid, mlist):
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
    }

    requests.insert(query)


def update_request(id, type, cid, mlist):
    query = {
        'type': type,
        'cid': cid,
        'mlist': mlist,
    }

    requests.update(query, doc_ids=[id])

def delete_request(cid, type):
    Request = Query()
    return requests.remove(cond=(Request.cid==cid) & (Request.type==type))

def get_request_query(cid, type):
    Request = Query()
    requestq =  requests.get(cond=(Request.cid==cid) & (Request.type==type))

    return requestq


def get_orders():
    return orders.all()
