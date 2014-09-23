# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from datetime import datetime
from datetime import timedelta
from pyramid.view import view_config

from core import Entity

DEFAULT_SESSION_TIME = 30
LOGGED_ACCOUNT_KEY = "logged_account"


class Sign(Entity):
    def fields(self):
        return ["_id", "whose", "category", "description", "timestamp"]


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
            account_id = str(account.id)
            work_time = ProfileService().find_work_time(account_id)
            signs_dict = SignService().find_out_yesterday_today_sign(account_id)
            result = {'work_start': work_time.get('work_start'),
                      'work_end': work_time.get('work_end'),
                      'yesterday_start': signs_dict.get('yesterday_start'),
                      'yesterday_end': signs_dict.get('yesterday_end'),
                      'today_start': signs_dict.get('today_start'),
                      'today_end': signs_dict.get('today_end')}
            time_fmt = "%H:%M:%S"
            if result['work_start'] is not None:
                result['work_start'] = result.get('work_start').strftime(time_fmt)
            if result['work_end'] is not None:
                result['work_end'] = result.get('work_end').strftime(time_fmt)
            if result['yesterday_start'] is not None:
                result['yesterday_start'] = result.get('yesterday_start').time().strftime(time_fmt)
            if result['yesterday_end'] is not None:
                result['yesterday_end'] = result.get('yesterday_end').time().strftime(time_fmt)
            if result['today_start'] is not None:
                result['today_start'] = result.get('today_start').time().strftime(time_fmt)
            if result['today_end'] is not None:
                result['today_end'] = result.get('today_end').time().strftime(time_fmt)
            return {'result': result}


class SignService:
    def __init__(self):
        self.__storage = SignStorage()

    def find_out_yesterday_today_sign(self, behavior_id):
        today = datetime.now()
        yesterday = today.replace(day=today.day - 1)
        t_start_sign, t_end_sign = self.__storage.retrieve_first_last(behavior_id,
                                                                      today.replace(hour=5, minute=0, second=0),
                                                                      today.replace(hour=23, minute=59, second=59))
        y_start_sign, y_end_sign = self.__storage.retrieve_first_last(behavior_id,
                                                                      yesterday.replace(hour=5, minute=0, second=0),
                                                                      yesterday.replace(hour=23, minute=59, second=59))
        result_dict = dict()
        if t_start_sign is not None:
            result_dict['today_start'] = t_start_sign.timestamp
        if t_end_sign is not None:
            result_dict['today_end'] = t_end_sign.timestamp
        if y_start_sign is not None:
            result_dict['yesterday_start'] = y_start_sign.timestamp
        if y_end_sign is not None:
            result_dict['yesterday_end'] = y_end_sign.timestamp
        return result_dict

    def find_out_mouth_signs(self, behavior_id):
        now = datetime.now()
        mouth_start = now.replace(day=1, hour=0, minute=0, second=0)
        mouth_end = mouth_start.replace(month=mouth_start.month+1, day=1, hour=23, minute=59, second=59)
        mouth_end -= timedelta(days=1)
        return self.__storage.list_sign_from_to(behavior_id, mouth_start, mouth_end)


class SignStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.sign

    def create(self, sign):
        assert isinstance(sign, Sign), "Parameter 'sign' type error, should be core.Sign"
        from datetime import datetime
        sign.timestamp = datetime.now()
        self.__mongo.insert(sign.__dict__)
        return sign

    def retrieve(self, key="_id", value=None):
        sign_dict = {key: value}
        self.__mongo.find_one(sign_dict)
        return Sign(sign_dict)

    def retrieve_first_last(self, behavior, from_, to):
        from core import Constraint
        c = Constraint('whose', '=', behavior)
        c &= Constraint('timestamp', '>', from_)
        c &= Constraint('timestamp', '<', to)
        iterable = self.__mongo.find(c.value).sort('timestamp', 1)
        size = iterable.count()
        if size is 1:
            return Sign(iterable[0]), None
        if size > 1:
            return Sign(iterable[0]), Sign(iterable[size-1])
        else:
            return None, None

    def list_sign_from_to(self, behavior, from_, to):
        from core import Constraint
        c = Constraint('whose', '=', behavior)
        c &= Constraint('timestamp', '=', from_)
        c &= Constraint('timestamp', '=', to)
        iterable = self.__mongo.find(c.value).sort('timestamp', 1)
        result_list = list()
        if iterable is None or iterable.count() is 0:
            return result_list
        for sign_dict in iterable:
            result_list.append(Sign(sign_dict))
        return result_list

    def update(self, sign):
        assert isinstance(sign, Sign), "Parameter 'sign' type error, should be core.Sign"
        assert sign.id is not None, "Cannot update for not exist sign"
        from datetime import datetime
        sign.updated_at = datetime.now()
        self.__mongo.update({'_id': sign.id}, sign.__dict__)
        return sign

    def delete(self, sign):
        assert isinstance(sign, Sign), "Parameter 'sign' type error, should be core.Sign"
        self.__mongo.remove(sign.__dict__)
        return sign