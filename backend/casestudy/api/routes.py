from datetime import datetime
from casestudy.api import securities, users, auth

ROUTES = {
    '/v1/users/<int:userId>/watch_list': (users.get_users_watch_list, ['GET']),
    '/v1/users/<int:userId>/watch_list/': (users.post_users_watch_list, ['POST', 'DELETE']),
    '/v1/securities/search': (securities.search_securities, ['GET']),
    '/v1/securities': (securities.get_securities, ['GET']),
    '/v1/login/': (auth.authenticate, ['POST'])
}