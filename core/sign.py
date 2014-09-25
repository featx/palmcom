# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from datetime import timedelta
from datetime import time
from datetime import datetime

from pyramid.view import view_config
from mongoengine import *

from core.account import Account

DEFAULT_SESSION_TIME = 30
LOGGED_ACCOUNT_KEY = "logged_account"


class Sign(Document):
    whose = ReferenceField(Account)
    category = StringField(max_length=255)
    description = StringField()
    timestamp = DateTimeField()

    meta = {'indexes': ['timestamp'],
            'ordering': ['timestamp']}


class SignSurface:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='duty', renderer='json')
    def duty_situation(self):
        account = self.request.session.get(LOGGED_ACCOUNT_KEY, None)
        if account is None:
            return {'result': {'msg': "Please login first", 'error': ''}}
        else:
            from core.profile import ProfileService
            work_start, work_end = ProfileService.find_work_time(account)
            today_start, today_end, yestoday_start, yestoday_end \
                = SignService.find_out_yesterday_today_signs(account)
            time_fmt = "%H:%M:%S"
            result = {'work_start': work_start.strftime(time_fmt),
                      'work_end': work_end.strftime(time_fmt),
                      'yesterday_start': yestoday_start.time().strftime(time_fmt),
                      'yesterday_end': yestoday_end.time().strftime(time_fmt),
                      'today_start': today_start.time().strftime(time_fmt),
                      'today_end': today_end.time().strftime(time_fmt)}
            return {'result': result}


def extract_timestamp(sign, default=datetime(1900, 1, 1, 0, 0, 0)):
    if sign is None:
        return default
    else:
        return sign.timestamp


class SignService:

    @classmethod
    def find_out_yesterday_today_signs(cls, account):
        today = datetime.now()
        yesterday = today.replace(day=today.day - 1)
        t_start_sign = Sign.objects(whose=account, timestamp__gt=today.replace(hour=5, minute=0, second=0)).first()
        t_end_sign = Sign.objects.order_by('-timestamp')\
            .filter(whose=account, timestamp__lt=today.replace(hour=23, minute=59, second=59)).first()
        y_start_sign = Sign.objects(whose=account, timestamp__gt=yesterday.replace(hour=5, minute=0, second=0)).first()
        y_end_sign = Sign.objects.order_by('-timestamp')\
            .filter(whose=account, timestamp__lt=yesterday.replace(hour=23, minute=59, second=59)).first()
        ts = extract_timestamp(t_start_sign)
        te = extract_timestamp(t_end_sign)
        ys = extract_timestamp(y_start_sign)
        ye = extract_timestamp(y_end_sign)
        return ts, te, ys, ye

    @classmethod
    def find_out_mouth_signs(cls, account):
        mouth_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        mouth_end = mouth_start.replace(month=mouth_start.month+1, day=1, hour=23, minute=59, second=59)
        mouth_end -= timedelta(days=1)
        sign_list = Sign.objects.filter(whose=account, timestamp__gt=mouth_start, timestamp__lt=mouth_end)
        result = list()
        for sign in sign_list:
            sign_dict = dict()
            sign_dict['id'] = str(sign.id)
            sign_dict['category'] = sign.category
            sign_dict['description'] = sign.description
            sign_dict['time'] = sign.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            result.append(sign_dict)
        return result
