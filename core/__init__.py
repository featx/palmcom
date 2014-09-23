# -*- coding: utf-8 -*-
__author__ = 'palmtale'
import web

from pyramid.config import Configurator
from pymongo import MongoClient

mongo_db = None


def main(global_config, **settings):
    mongo_client = MongoClient(settings.get("mongodb_host", "localhost"), int(settings.get("mongodb_port", "27017")))
    global mongo_db
    mongo_db = mongo_client.palms
    assert mongo_db.authenticate(settings.get("mongodb_username", ""), settings.get("mongodb_password", "")), \
        "Mongo authentication error."

    config = Configurator(settings=settings)
    # I18N files
    config.add_translation_dirs("i18n:locale/")
    web.config(config)
    config.add_route('duty', '/duty')
    config.scan()
    return config.make_wsgi_app()


class Entity:
    def what(self):
        return type(self).__name__

    def fields(self):
        return ['_id']

    @property
    def id(self):
        return str(self._id)

    def __init__(self, _dict_=None):
        self._id = None
        if _dict_ is None or not isinstance(_dict_, dict):
            return
        _dict = _dict_.copy()
        fields = self.fields()
        for f in _dict_.keys():
            if not fields.__contains__(f):
                del _dict[f]
        self.__dict__ = _dict

    def to_dict(self):
        return self.__dict__.copy()


class Constraint:
    def __init__(self, name, compare, value,):
        self.__value = dict()
        if compare is "=" or compare is "==" or compare is "eq" or compare is "equals":
            self.__value = {name: value}
        if compare is "<>" or compare is "!=" or compare is "ne":
            self.__value = {"$ne": {name: value}}
        if compare is "<" or compare is "lt":
            self.__value = {"$lt": {name: value}}
        if compare is ">" or compare is "gt":
            self.__value = {"$gt": {name: value}}
        if compare is ">=" or compare is "gte":
            self.__value = {"$gte": {name: value}}
        if compare is "<=" or compare is "lte":
            self.__value = {"$lte": {name: value}}

    @property
    def value(self):
        return self.__value

    def copy(self):
        copy = Constraint('', '', '')
        copy.__value = self.__value.copy()
        return copy

    def __iand__(self, other):
        assert isinstance(other, Constraint), "Comparing object should be the type of Constraint"
        for k, v in other.value.items():
            self_v = self.__value.get(k)
            if isinstance(self_v, dict) and isinstance(v, dict):
                self_v.update(v)
            else:
                self.__value[k] = v
        return self

    def __and__(self, other):
        assert isinstance(other, Constraint), "Comparing object should be the type of Constraint"
        new_value = {}
        self_value = self.__value.copy()
        other_value = other.value.copy()
        for k, v in self_value.items():
            new_value[k] = v
        for k, v in other_value.items():
            _v = new_value.get(k)
            if isinstance(_v, dict) and isinstance(v, dict):
                _v.update(v)
            else:
                _v[k] = v
        c = Constraint('', '', '')
        c.__value = new_value
        return c

    def __ior__(self, other):
        assert isinstance(other, Constraint), "Comparing object should be the type of Constraint"
        OR = "$or"
        or_list = self.value.get(OR, None)
        if or_list is not None and len(self.value.keys()) is 1:
            or_list.append(other.value)
            return self
        or_list = other.value.get(OR, None)
        if or_list is not None and len(other.value.keys()) is 1:
            or_list.append(self.__value)
            self.__value = dict()
            self.__value[OR] = or_list
            return self
        self.__value = {OR: [self.__value, other.value]}
        return self

    def __or__(self, other):
        assert isinstance(other, Constraint), "Comparing object should be the type of Constraint"
        OR = "$or"
        or_list = self.__value.get(OR, None)
        if or_list is not None and len(self.__value.keys()) is 1:
            list_copy = or_list.copy()
            list_copy.append(other.value)
        else:
            ors_list = other.value.get('$or', None)
            if ors_list is not None and len(other.value.keys()) is 1:
                list_copy = or_list.copy()
                list_copy.append(self.__value)
            else:
                self_value = self.__value.copy()
                other_value = other.value.copy()
                list_copy = [self_value, other_value]
        c = Constraint('', '', '')
        c.__value[OR] = list_copy
        return c
