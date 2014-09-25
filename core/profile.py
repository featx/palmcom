# -*- coding: utf-8 -*-
__author__ = 'palmtale'
import logging
from datetime import datetime

from mongoengine import *

from core.account import Account


log = logging.getLogger(__name__)


class Profile(Document):
    whose = ReferenceField(Account, unique=True)
    avatar = FileField()
    work_start = DateTimeField(default=datetime.strptime("000000", "%H%M%S"))
    work_end = DateTimeField(default=datetime.strptime("000000", "%H%M%S"))
    created_at = DateTimeField()
    updated_at = DateTimeField()


class ProfileService:

    @classmethod
    def find_work_time(cls, account):
        try:
            profile = Profile.objects.only('work_start', 'work_end').get(whose=account)
            work_start = profile.work_start.time()
            work_end = profile.work_end.time()
        except Profile.DoesNotExist:
            log.warn("Find work time for not exist account %s ", account.id)
            work_start = datetime.strptime('000000', '%H%M%S').time()
            work_end = datetime.strptime('000000', '%H%M%S').time()
        return work_start, work_end

    @classmethod
    def set_work_time(cls, account, start, end):
        #profile = Profile.objects.only('id').get(whose=account)
        from datetime import datetime
        work_start = datetime.strptime(start, "%H:%M:%S")
        work_end = datetime.strptime(end, "%H:%M:%S")
        Profile.objects.only('id').get_or_create(whose=account)
        Profile.objects(whose=account).update_one(set__work_start=work_start, set__work_end=work_end)

