# -*- coding: utf-8 -*-
__author__ = 'Cartoon'
from core import MONGO_ID_STR


class Avatar:
    id = None
    data = ""
    whose = None
    create_at = None
    update_at = None


def new_avatar_from_dict(dict_):
    avatar = Avatar()
    if dict_ is not None and isinstance(dict_, dict):
        avatar.id = dict_.get('id', None)
        avatar.data = dict_.get('data', None)
        avatar.whose = dict_.get('whose', None)
        avatar.create_at = dict_.get('create_at', None)
        avatar.update_at = dict_.get('update_at', None)
    return avatar


class AvatarStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.avatar

    def create(self, avatar):
        assert self.retrieve(avatar.whose) is None, "Some serialize field is existed"
        avatar.id = None
        from datetime import datetime
        avatar.create_at = datetime.now()
        avatar.update_at = avatar.create_at
        return self.__mongo.insert(avatar.__dict__)

    def retrieve(self, whose):
        _dict_ = self.__mongo.retrieve({'whose': whose})
        if _dict_ is not None:
            _dict_['id'] = _dict_.get('_id')
            del _dict_['_id']
            return new_avatar_from_dict(_dict_)
        return None

    def update(self, avatar):
        if avatar is None or avatar.id is None or avatar.id.strip() is "":
            return
        _id = avatar.id
        avatar.id = None
        self.__mongo.update({MONGO_ID_STR: _id}, avatar.__dict__)

    def delete(self, avatar):
        if avatar is None or avatar.id is None or avatar.id.strip() is "":
            return
        _dict = avatar.__dict__
        _dict[MONGO_ID_STR] = _dict['id']
        del _dict['id']
        self.__mongo.remove(_dict)