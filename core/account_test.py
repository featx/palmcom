# -*- coding: utf-8 -*-
__author__ = 'palmtale'

import unittest
from hashlib import md5

from mongoengine import *
from mongoengine.context_managers import switch_db

from core.account import Account as _Account
from core.account import AccountService


class AccountTest(unittest.TestCase):
    def setUp(self):
        connect('palms', username='palms', password='palms')
        connect('palms_test', alias="test", username='test', password='test')

    def tearDown(self):
        with switch_db(_Account, 'test') as Account:
            Account.drop_collection()
        a = AccountService.find_out_account("2014090801", '123456')
        if a is None:
            _Account(work_id="2014090801", username="palmtale", email="palmtale@live.com",
                     cell_phone_number="13303030033",
                     password=md5(bytes('123456', 'utf8')).hexdigest().upper()).save()

    def test(self):
        with switch_db(_Account, 'test') as Account:
            account = Account(work_id="201401204", username="palmtale", email="palmtale@live.com",
                              cell_phone_number="13300130013")
            password = "123456"
            account.password = md5(bytes(password, "utf8")).hexdigest().upper()
            account.save()
            a = AccountService.find_out_account("201401204", "123456")
            self.assertEqual(account.id, a.id)
            aa = AccountService.find_out_account("palmtale", "123456")
            self.assertEqual(account.id, aa.id)
            aaa = AccountService.find_out_account("palmtale@live.com", "123456")
            self.assertEqual(account.id, aaa.id)
            aaaa = AccountService.find_out_account("13300130013", "123456")
            self.assertEqual(account.id, aaaa.id)


if __name__ == "__main__":
    unittest.main()