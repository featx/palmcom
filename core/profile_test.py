# -*- coding: utf-8 -*-
__author__ = 'palmtale'

import unittest
from mongoengine import *

from core.account import Account
from core.profile import Profile


class ProfileTest(unittest.TestCase):

    def setUp(self):
        connect('palms_test', username='test', password='test')

    def tearDown(self):
        Account.drop_collection()
        Profile.drop_collection()

    def test_work_time(self):
        from core.profile import ProfileService
        from core.account import AccountService
        from hashlib import md5
        account = Account(work_id="201409221941",
                          username="palmtale",
                          password=md5(bytes("123456", "utf8")).hexdigest().upper(),
                          email="palmtale@dd.com",
                          cell_phone_number="1233112321")
        account.save()
        a = AccountService.find_out_account('palmtale', '123456')
        self.assertIsNotNone(a, "Test error caused by the account did not found")
        ProfileService.set_work_time(a, "09:00:00", "18:00:00")
        work_start, work_end = ProfileService.find_work_time(a)
        from datetime import datetime
        self.assertEqual(work_start, datetime.strptime("090000", "%H%M%S").time())
        self.assertEqual(work_end, datetime.strptime("180000", "%H%M%S").time())


if __name__ == '__main__':
    unittest.main()
