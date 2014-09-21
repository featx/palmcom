# -*- coding: utf-8 -*-
__author__ = 'palmtale'

import core
import unittest
from pymongo import MongoClient
from core import sign,account


class SignMongoTest(unittest.TestCase):
    def setUp(self):
        mongo_client = MongoClient()
        core.mongo_db = mongo_client.palms_test
        core.mongo_db.authenticate("test", "test")
        self.__account_storage = account.AccountStorage()
        user = account.Account()
        user.username = 'palmtale'
        self.__account_storage.create(user)
        self.user = self.__account_storage.retrieve(user)
        self.__storage = sign.SignStorage()

    def tearDown(self):
        core.mongo_db.drop_collection('account')
        core.mongo_db.drop_collection('sign')

    def test_retrieve_from_to(self):
        from datetime import datetime
        now = datetime.now()
        sign_1 = sign.Sign()
        sign_1.behavior = self.user.id
        sign_1.timestamp = now.replace(hour=1)
        sign_2 = sign.Sign()
        sign_2.behavior = self.user.id
        sign_2.timestamp = now.replace(hour=2, minute=1)
        sign_3 = sign.Sign()
        sign_3.behavior = self.user.id
        sign_3.timestamp = now.replace(hour=3)
        sign_4 = sign.Sign()
        sign_4.behavior = self.user.id
        sign_4.timestamp = now.replace(hour=4)
        self.__storage.create(sign_1)
        self.__storage.create(sign_2)
        self.__storage.create(sign_3)
        self.__storage.create(sign_4)
        reuslt_set = self.__storage.retrieve_from_to(self.user.id, now.replace(hour=2, minute=0), now.replace(hour=4, minute=0))
        for item in reuslt_set:
            print(item)

if __name__ == '__main__':
    unittest.main()
