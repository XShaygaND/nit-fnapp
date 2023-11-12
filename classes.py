from storage import save_user, update_user, save_request, delete_request
from typing import Union


class Order:
    def __init__(self, id: int = None, uid: int = None, did: int = None, status: int = None, location: str = None, payment_mid: int = None, student_code: int = None, password: int = None):
        self.id = id
        self.uid = uid
        self.did = did
        self.status = status
        self.location = location
        self.payment_mid = payment_mid
        self.student_code = student_code
        self.password = password


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
            self.id,
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
    def __init__(self, id: int = None, type:str = None, cid: int = None, mid:int = None, mlist:Union[int, dict] = None):
        self.id = id
        self.type = type
        self.cid = cid
        self.mid = mid
        self.mlist = mlist

    def save(self):
        save_request(
            type=self.type,
            cid=self.cid,
            mid=self.mid,
            mlist=self.mlist,
        )

    def delete(self):
        delete_request(self.cid)
