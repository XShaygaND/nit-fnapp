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


def save_order(cid, customer_name, student_code, password, food_code, payment_image, status_code):
    query = {
        'cid': cid,
        'customer_name': customer_name,
        'student_code': student_code,
        'password': password,
        'food_code': food_code,
        'payment_image': payment_image,
        'status_code': status_code,
    }

    return orders.insert(query)


def update_order(oid, cid, customer_name, student_code, password, food_code, payment_image, status_code):
    query = {
        'cid': cid,
        'customer_name': customer_name,
        'student_code': student_code,
        'password': password,
        'food_code': food_code,
        'payment_image': payment_image,
        'status_code': status_code,
    }

    return orders.update(query, doc_ids=[oid])


def save_image(file, filename):
    with open(f'{image_dir}{filename}.png', 'wb') as new_file:
        new_file.write(file)


def get_mod_list():
    UserQ = Query()
    mod_usersq = users.search(UserQ.is_mod==True)

    return mod_usersq

def save_request(type, cid, mid, mlist):
    query = {
        'type': type,
        'cid': cid,
        'mid': mid,
        'mlist': mlist,
    }

    requests.insert(query)


def delete_request(cid):
    RequestQ = Query()
    return requests.remove(RequestQ.cid==cid)

def get_request_query(cid, type):
    RequestQ = Query()
    requestsq =  requests.get(cond=(RequestQ.cid==cid) & (RequestQ.type==type))

    return requestsq


def get_orders():
    return orders.all()
