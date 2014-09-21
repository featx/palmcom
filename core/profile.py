# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from core import MONGO_ID_STR


class ProfileService:
    def __init__(self):
        self.__storage = ProfileStorage()

    def find_work_time(self, account_id):
        work_time = self.__storage.retrieve_work_time(account_id)
        if work_time is None:
            work_time = dict()
        else:
            work_time['work_start'] = work_time.get('work_start').time()
            work_time['work_end'] = work_time.get('work_end').time()
        return work_time

    def set_work_time(self, account_id, start, end):
        profile = self.__storage.retrieve(str(account_id))
        if profile is None:
            profile = Profile()
        profile.whose = str(account_id)
        from datetime import datetime
        profile.work_start = datetime.strptime(start, "%H:%M:%S").time()
        profile.work_end = datetime.strptime(end, "%H:%M:%S").time()
        self.__storage.create(profile)


class Profile:
    id = None
    whose = None
    avatar = None
    work_start = None
    work_end = None
    created_at = None
    updated_at = None


def new_profile_from_dict(dict_):
    profile = Profile()
    if dict_ is not None and isinstance(dict_, dict):
        profile.id = dict_.get('id', None)
        profile.avatar = dict_.get('avatar', None)
        profile.whose = dict_.get('whose', None)
        profile.work_start = dict_.get("work_start", None)
        profile.work_end = dict_.get("work_end", None)
        profile.create_at = dict_.get('create_at', None)
        profile.update_at = dict_.get('update_at', None)
    return profile


class ProfileStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.profile

    def create(self, profile):
        assert self.retrieve(profile.whose) is None, "Some serialize field is existed"
        profile.id = None
        from datetime import datetime
        profile.create_at = datetime.now()
        profile.update_at = profile.create_at
        return self.__mongo.insert(profile.__dict__)

    def retrieve(self, account_id):
        _dict_ = self.__mongo.find({'whose': account_id})
        if _dict_ is not None:
            _dict_['id'] = _dict_.get('_id')
            del _dict_['_id']
            return new_profile_from_dict(_dict_)
        return None

    def retrieve_avatar(self, account_id):
        result = self.__mongo.find({'whose': account_id}, {MONGO_ID_STR: False, 'avatar': True})
        return result[0]['avatar']

    def retrieve_work_time(self, account_id):
        result_set = self.__mongo.find({'whose': account_id},
                                       {MONGO_ID_STR: False, 'work_start': True, 'work_end': True})
        if result_set is None or result_set.count() is 0:
            return None
        else:
            return result_set[0]