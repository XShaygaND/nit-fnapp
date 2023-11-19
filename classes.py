from storage import save_user, update_user, save_request, update_request, delete_request, save_order, update_order, delete_order
from datatypes import OrderType
from datatypes import RequestType


class Order:
    def __init__(self, id: int = None, uid: int = None, did: int = None, status: int = None, meal: OrderType = None, location: str = None, payment_mid: int = None, student_code: int = None, password: int = None, verification_code: int = None):
        self.id = id
        self.uid = uid
        self.did = did
        self.status = status
        self.meal = meal
        self.location = location
        self.payment_mid = payment_mid
        self.student_code = student_code
        self.password = password
        self.verification_code = verification_code

    def save(self):
        save_order(
            uid = self.uid,
            did = self.did,
            status = self.status,
            meal = self.meal,
            location = self.location,
            payment_mid = self.payment_mid,
            student_code = self.student_code,
            password = self.password,
            verification_code = self.verification_code,
        )
    
    def update(self):
        update_order(
            id=self.id,
            uid=self.uid,
            did=self.did,
            status=self.status,
            meal=self.meal,
            location=self.location,
            payment_mid=self.payment_mid,
            student_code=self.student_code,
            password=self.password,
            verification_code=self.verification_code
        )
    
    def delete(self):
        delete_order(self.uid, self.meal)


class User:
    def __init__(self, id: int = None, cid: int = None, name: str = None, order_count: int = 0, enabled: bool = True, in_command: bool = False, warns: int = 0, is_sudo: bool = False, is_mod=False):
        self.id = id
        self.cid = cid
        self.name = name
        self.enabled = enabled
        self.order_count = order_count
        self.in_command = in_command
        self.warns = warns
        self.is_sudo = is_sudo
        self.is_mod = is_mod

    def save(self):
        save_user(
            cid=self.cid,
            name=self.name,
            enabled=self.enabled,
            order_count=self.order_count,
            warns=self.warns,
            is_sudo=self.is_sudo,
            is_mod=self.is_mod,
        )
    
    def update(self):
        update_user(
            id=self.id,
            cid=self.cid,
            name=self.name,
            enabled=self.enabled,
            order_count=self.order_count,
            warns=self.warns,
            is_sudo=self.is_sudo,
            is_mod=self.is_mod,
        )


class Delivery:
    def __init__(self, id: int = None, uid: int = None, orders: dict = None, total_deliveries: int = None, deliveries: dict = None):
        self.id = id
        self.uid = uid
        self.orders = orders
        self.total_deliveries = total_deliveries
        self.deliveries = deliveries


class Request:
    def __init__(self, id: int = None, type:str = None, cid: int = None, mlist:list = None):
        self.id = id
        self.type = type
        self.cid = cid
        self.mlist = mlist

    def save(self):
        save_request(
            type=self.type,
            cid=self.cid,
            mlist=self.mlist,
        )

    def update(self):
        update_request(
            id=self.id,
            type=self.type,
            cid=self.cid,
            mlist=self.mlist
        )

    def delete(self):
        delete_request(self.cid, self.type)
