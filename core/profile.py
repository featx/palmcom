# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from core import Entity


class Profile(Entity):
    def fields(self):
        return ["_id", "whose", "avatar", "work_start", "work_end", "created_at", "updated_at"]


class ProfileService:
    def __init__(self):
        self.__storage = ProfileStorage()

    def find_work_time(self, account_id):
        work_time = self.__storage.retrieve_work_time(account_id)
        from datetime import datetime
        for k, v in work_time.items():
            if not isinstance(v, datetime):
                continue
            work_time[k] = v.time()
        return work_time

    def set_work_time(self, account_id, start, end):
        profile = self.__storage.retrieve(key='whose', value=str(account_id))
        if profile is None:
            profile = Profile()
            profile.whose = str(account_id)
        from datetime import datetime
        profile.work_start = datetime.strptime(start, "%H:%M:%S").time()
        profile.work_end = datetime.strptime(end, "%H:%M:%S").time()
        self.__storage.create_or_update(profile)


class ProfileStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.profile

    def create(self, profile):
        assert isinstance(profile, Profile), "Parameter 'profile' type error, should be core.Profile"
        from datetime import datetime
        profile.timestamp = datetime.now()
        self.__mongo.insert(profile.__dict__)
        return profile

    def retrieve(self, key='_id', value=None):
        profile_dict = {key: value}
        self.__mongo.find_one(profile_dict)
        return Profile(profile_dict)

    def retrieve_avatar(self, account_id):
        result = self.__mongo.find({'whose': account_id}, {'_id': False, 'avatar': True})
        return result[0]['avatar']

    def retrieve_work_time(self, account_id):
        result_set = self.__mongo.find({'whose': account_id},
                                       {'_id': False, 'work_start': True, 'work_end': True})
        if result_set is None or result_set.count() is 0:
            return dict()
        else:
            return result_set[0]

    def update(self, profile):
        assert isinstance(profile, Profile), "Parameter 'sign' type error, should be core.Sign"
        assert profile.id is not None, "Cannot update for not exist profile"
        from datetime import datetime
        profile.updated_at = datetime.now()
        self.__mongo.update({'_id': profile.id}, profile.__dict__)
        return profile

    def delete(self, profile):
        assert isinstance(profile, Profile), "Parameter 'sign' type error, should be core.Sign"
        self.__mongo.delete(profile.__dict__)
        return profile

    def create_or_update(self, profile):
        assert isinstance(profile, Profile), "Parameter 'sign' type error, should be core.Sign"
        if profile.id is None:
            return self.create(profile)
        else:
            return self.update(profile)

