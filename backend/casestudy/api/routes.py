from datetime import datetime
from casestudy.api import securities, users, auth

ROUTES = {
    '/v1/users/<int:userId>/watch_list': (users.get_user_watch_list, ['GET']),
    '/v1/users/<int:userId>/watch_list/': (users.post_security_to_user_watchlist, ['POST']),
    '/v1/users/<int:userId>/watch_list/<int:securityId>': (users.delete_security_user_watchlist, ['DELETE']),
    '/v1/securities/search': (securities.search_securities, ['GET']),
    '/v1/securities/<int:securityId>': (securities.get_security_info, ['GET']),
    '/v1/login/': (auth.login, ['POST'])
}
