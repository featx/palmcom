# -*- coding: utf-8 -*-
__author__ = 'palmtale'

from pyramid.config import Configurator
from pymongo import MongoClient

mongo_db = None
MONGO_ID_STR = "_id"


def main(global_config, **settings):
    # Taobao config add
    mongo_client = MongoClient(settings.get("mongodb_host", "localhost"), int(settings.get("mongodb_port", "27017")))
    global mongo_db
    mongo_db = mongo_client.palms
    assert mongo_db.authenticate(settings.get("mongodb_username", ""), settings.get("mongodb_password", "")), \
        "Mongo authentication error."
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    # I18N files
    config.add_translation_dirs("i18n:locale/")
    import web
    web.config(config)
    config.add_route('duty', '/duty')
    config.scan()
    return config.make_wsgi_app()


def to_mongo_dict(obj):
    _dict_ = obj.__dict__
    assert obj is not None, "Object is none while to mongo dict"
    if obj.id is not None:
        _dict_[MONGO_ID_STR] = obj.id
        del _dict_['id']
        return _dict_
    else:
        return dict()
