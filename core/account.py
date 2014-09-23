# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from hashlib import md5
from core import Entity
from core import Constraint


class Account(Entity):
    def fields(self):
        return ["_id", "work_id", "username", "password",
                "display_name", "first_name", "last_name",
                "gender", "age", "email", "cell_phone_number",
                "civil_id", "title", "position", "created_at",
                "updated_at"]


class AccountSurface:
    def __init__(self, request):
        self.request = request
        self.__service = AccountService()


class AccountService:
    def __init__(self):
        self.__storage = AccountStorage()

    def find_out_account(self, user_identity, password):
        password = md5(bytes(password, 'utf8')).hexdigest().upper()
        c = Constraint('username', '=', user_identity)
        c |= Constraint('email', '=', user_identity)
        c |= Constraint('cell_phone_number', '=', user_identity)
        c &= Constraint('password', '=', password)
        return self.__storage.retrieve_as_constraint(c)


#Mongo:
class AccountStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.account

    def exist_same_unique_field(self, _account_):
        account = _account_
        if isinstance(_account_, dict):
            account = Account(_account_)
        conditions = list()
        if account.work_id is not None and account.work_id.strip() is not "":
            conditions.append({'work_id': account.work_id})
        if account.username is not None and account.username.strip() is not "":
            conditions.append({'username': account.username})
        if account.email is not None and account.email.strip() is not "":
            conditions.append({'email': account.email})
        if account.cell_phone_number is not None and account.cell_phone_number.strip() is not "":
            conditions.append({'cell_phone_number': account.cell_phone_number})
        if conditions.__len__ is 0:
            return False
        if self.__mongo.find_one({'$or': conditions}) is None:
            return False
        else:
            return True

    def create(self, account):
        assert isinstance(account, Account), "Parameter 'account' type error, should be core.Account"
        assert account.id is None, "Id should be none for creating entity"
        from datetime import datetime
        account.created_at = datetime.now()
        account.updated_at = datetime.now()
        self.__mongo.insert(account.__dict__)
        return account

    def retrieve(self, key="_id", value=None):
        account_dict = {key: value}
        self.__mongo.find_one(account_dict)
        return Account(account_dict)

    def retrieve_as_constraint(self, constraint):
        assert isinstance(constraint, Constraint), "Parameter dict_condition should be type core.constraint"
        constraint_dict = constraint.value.copy()
        self.__mongo.find_one(constraint_dict)
        return Account(constraint_dict)

    def update(self, account):
        assert isinstance(account, Account), "Parameter 'account' type error, should be core.Account"
        assert account.id is not None, "Cannot update for not exist account"
        from datetime import datetime
        account.updated_at = datetime.now()
        self.__mongo.update({'_id': account.id}, account.__dict__)
        return account

    def delete(self, account):
        assert isinstance(account, Account), "Parameter 'account' type error, should be core.Account"
        self.__mongo.remove(account.__dict__)
        return account
