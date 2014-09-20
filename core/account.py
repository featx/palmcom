# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from hashlib import md5
from core import to_mongo_dict
from core.avatar import AvatarStorage


class AccountSurface:
    def __init__(self, request):
        self.request = request
        self.__service = AccountService()


class AccountService:
    def __init__(self):
        self.__storage = AccountStorage()
        self.__avatar_storage = AvatarStorage()

    def find_out_account(self, user_identity, password):
        user_identities = [{'username': user_identity},
                           {'email': user_identity},
                           {'cell_phone_number': user_identity}]
        password = md5(bytes(password, 'utf8')).hexdigest().upper()
        dict_condition = {'password': password, '$or': user_identities}
        return self.__storage.retrieve_as_dict_condition(dict_condition)


class Account:
    id = None
    work_id = None
    username = None
    password = None
    display_name = None
    first_name = None
    last_name = None
    gender = None
    age = None
    email = None
    cell_phone_number = None
    civil_id = None
    title = None
    position = None
    create_at = None
    update_at = None


def new_account_from_dict(dict_):
    account = Account()
    if dict_ is not None and isinstance(dict_, dict):
        account.id = dict_.get('id', None)
        account.work_id = dict_.get('work_id', None)
        account.username = dict_.get('username', None)
        account.password = dict_.get('password', None)
        account.display_name = dict_.get('display_name', None)
        account.first_name = dict_.get('first_name', None)
        account.last_name = dict_.get('last_name', None)
        account.gender = dict_.get('gender', None)
        account.age = dict_.get('age', None)
        account.email = dict_.get('email', None)
        account.cell_phone_number = dict_.get('cell_phone_number', None)
        account.civil_id = dict_.get('civil_id', None)
        account.title = dict_.get('title', None)
        account.position = dict_.get('position', None)
        account.create_at = dict_.get('create_at', None)
        account.update_at = dict_.get('update_at', None)
    return account


#Mongo:
class AccountStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.account

    def create(self, account):
        assert not self.exist_same_unique_field(account), "Some account identity field is duplicated"
        account.id = None
        from datetime import datetime
        account.create_at = datetime.now()
        account.update_at = account.create_at
        return self.__mongo.insert(account.__dict__)

    def exist_same_unique_field(self, account):
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

    def retrieve(self, account):
        assert isinstance(account, Account), "Parameter account is incorrect type, should be Account"
        account_dict = self.__mongo.find_one(to_mongo_dict(account))
        if account_dict is not None:
            account_dict['id'] = account_dict.get('_id')
            del account_dict['_id']
            return new_account_from_dict(account_dict)
        return None

    def retrieve_as_dict_condition(self, dict_conditioin):
        assert isinstance(dict_conditioin, dict), "Parameter dict_condition should be type dict"
        account_dict = self.__mongo.find_one(dict_conditioin)
        if account_dict is not None:
            account_dict['id'] = account_dict.get('_id')
            del account_dict['_id']
            return new_account_from_dict(account_dict)
        return None

    def delete(self, account):
        assert isinstance(account, Account), "Parameter account is incorrect type, should be Account"
        return self.__mongo.remove(to_mongo_dict(account))

    def update(self, account):
        assert isinstance(account, Account), "Parameter account is incorrect type, should be Account"
        import time
        account.update_at = time.time()
        return self.__mongo.update(to_mongo_dict(account))
