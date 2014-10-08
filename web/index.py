# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPTemporaryRedirect
from pyramid.httpexceptions import HTTPUnauthorized

from core.account import AccountService
from core.sign import SignService

DEFAULT_SESSION_TIME = 30
LOGGED_ACCOUNT_KEY = "logged_account"


class IndexView:
    def __init__(self, request):
        self.request = request
        self.username = self.request.params.get('username', None)

    @view_config(route_name='login', renderer='templates/login.pt')
    def login(self):
        return {'username': self.username}

    @view_config(route_name='index', renderer='templates/index.pt')
    def index(self):
        if self.username is None:
            account = self.request.session.get(LOGGED_ACCOUNT_KEY, None)
        else:
            password = self.request.params.get('password', None)
            account = AccountService.find_out_account(self.username, password)
        if account is None:
            return HTTPTemporaryRedirect(location="/in.log")
        else:
            self.request.session[LOGGED_ACCOUNT_KEY] = account
            return {}

    @view_config(route_name="duties", renderer="templates/duties.pt")
    def duties(self):
        account = self.request.session.get(LOGGED_ACCOUNT_KEY, None)
        if account is None:
            return HTTPUnauthorized()
        sign_list = SignService.find_out_mouth_signs(account)
        dict_list = list()
        for sign in sign_list:
            dict_list.append(sign)
        return {'duties': dict_list}