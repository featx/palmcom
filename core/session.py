# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from pyramid.view import view_config


class SessionSurface:
    USERNAME_KEY = "username"
    PASSWORD_KEY = "password"
    LOGGED_USER_KEY = "logged_user"

    def __init__(self, request):
        self.request = request
        self.session = request.session

    def authenrize(self):
        username = self.request.params.get(SessionSurface.USERNAME_KEY, None)
        password = self.request.params.get(SessionSurface.PASSWORD_KEY, None)
        #Find account to pass the
        self.session[SessionSurface.LOGGED_USER_KEY] = "LoggedUser"
        return {}
