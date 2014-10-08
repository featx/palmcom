# -*- coding: utf-8 -*-
__author__ = 'palmtale'
import logging
from hashlib import md5
from mongoengine import *


log = logging.getLogger(__name__)


class Account(Document):
    work_id = StringField(unique=True)
    username = StringField(unique=True)
    password = StringField()
    display_name = StringField()
    first_name = StringField()
    last_name = StringField()
    gender = StringField()
    age = IntField(default=18)
    email = EmailField(unique=True)
    cell_phone_number = StringField(unique=True)
    civil_id = StringField()
    title = StringField()
    position = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()


class AccountSurface:
    def __init__(self, request):
        self.request = request


class AccountService:

    @classmethod
    def find_out_account(cls, user_identity, password):
        password = md5(bytes(password, 'utf8')).hexdigest().upper()
        q1 = Q(work_id=user_identity) | Q(username=user_identity) |\
             Q(email=user_identity) | Q(cell_phone_number=user_identity)
        q2 = Q(password=password) & q1
        try:
            rs = Account.objects.get(q2)
            return rs
        except Account.DoesNotExist:
            log.warn("Account is not existed for identity: " + user_identity + " with the input password")
            return None