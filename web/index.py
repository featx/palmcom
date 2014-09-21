# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPTemporaryRedirect
from core.account import AccountService
DEFAULT_SESSION_TIME = 30
LOGGED_ACCOUNT_KEY = "logged_account"


class IndexView:
    def __init__(self, request):
        self.request = request
        self.__account_service = AccountService()
        self.__logged_user = None
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
            account = self.__account_service.find_out_account(self.username, password)
        if account is None:
            return HTTPTemporaryRedirect(location="/in.log")
        else:
            self.request.session[LOGGED_ACCOUNT_KEY] = account
            self.__logged_user = account
            return {}

    @view_config(route_name='duty', renderer='json')
    def duty_situation(self):
        account = self.request.session.get(LOGGED_ACCOUNT_KEY, None)
        if account is None:
            return {'result': {'msg': "Please login first", 'error': ''}}
        else:
            from core.profile import ProfileService
            from core.sign import SignService
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