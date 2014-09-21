# -*- coding: utf-8 -*-
__author__ = 'palmtale'


class SignService:
    def __init__(self):
        self.__storage = SignStorage()

    def find_out_yesterday_today_sign(self, behavior_id):
        from datetime import datetime
        today = datetime.now()
        yesterday = today.replace(day=today.day - 1)
        today_sign = self.__storage.retrieve_from_to(behavior_id,
                                                     today.replace(hour=5, minute=0, second=0),
                                                     today.replace(hour=23, minute=59, second=59))
        yesterday_sign = self.__storage.retrieve_from_to(behavior_id,
                                                         yesterday.replace(hour=5, minute=0, second=0),
                                                         yesterday.replace(hour=23, minute=59, second=59))
        result_dict = dict()
        if len(today_sign) > 0:
            result_dict['today_start'] = today_sign[0].get('timestamp')
        if len(today_sign) > 1:
            result_dict['today_end'] = today_sign[1].get('timestamp')
        if len(yesterday_sign) > 0:
            result_dict['yesterday_start'] = yesterday_sign[0].get('timestamp')
        if len(yesterday_sign) > 1:
            result_dict['yesterday_end'] = yesterday_sign[1].get('timestamp')
        return result_dict


class Sign:
    id = None
    behavior = None
    category = None
    description = None
    timestamp = None

    def force_dict(self, sign_dict):
        self.id = sign_dict.get('_id', None)
        self.behavior = sign_dict.get('behavior', None)
        self.category = sign_dict.get('category', None)
        self.description = sign_dict.get('description', None)
        self.timestamp = sign_dict.get('timestamp', None)


class SignStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.sign

    def __mongo_dict(self, sign):
        sign_dict = sign.to_dict()
        sign_id = sign_dict.get('id', None)
        if sign_id is not None:
            from core import MONGO_ID_STR
            sign_dict[MONGO_ID_STR] = sign_id
            sign_dict['id'] = None
        return sign_dict

    def create(self, sign):
        assert isinstance(sign, Sign), "Parameter should be the type Sign"
        from datetime import datetime
        sign.timestamp = datetime.now()
        return self.__mongo.insert(sign.__dict__)

    def retrieve(self, sign):
        sign_dict = self.__mongo.find_one(self.__mongo_dict(sign))
        sign = Sign()
        sign.force_dict(sign_dict)
        return sign

    def retrieve_from_to(self, behavior, from_, to):
        retrieve_condition = {'behavior': behavior, 'timestamp': {'$gt': from_, '$lt': to}}
        iterable = self.__mongo.find(retrieve_condition).sort('timestamp', 1)
        size = iterable.count()
        if size is 1:
            return [iterable[0]]
        if size > 1:
            return [iterable[0], iterable[size-1]]
        else:
            return []

    def update(self, sign):
        self.__mongo.update(self.__mongo_dict(sign))

    def delete(self, sign):
        self.__mongo.delete(self.__mongo_dict(sign))
