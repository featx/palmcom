# -*- coding: utf-8 -*-
__author__ = 'palmtale'
import web

from pyramid.config import Configurator
from mongoengine import connect


def main(global_config, **settings):
    connect(settings.get("mongodb_default_db"),
            host=settings.get("mongodb_host"),
            port=int(settings.get("mongodb_port")),
            username=settings.get("mongodb_username"),
            password=settings.get("mongodb_password"))

    config = Configurator(settings=settings)
    # I18N files
    config.add_translation_dirs("i18n:locale/")
    web.config(config)
    config.add_route('duty', '/duty')
    config.scan()
    return config.make_wsgi_app()
