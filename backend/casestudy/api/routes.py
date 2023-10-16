from datetime import datetime
from casestudy.api import securities, users, auth
# Define available routes and associated functions and HTTP methods

ROUTES = {
    '/v1/users/<int:userId>/watch_list': (users.get_user_watch_list, ['GET']),
    '/v1/users/<int:userId>/watch_list/': (users.post_security_to_user_watchlist, ['POST']),
    '/v1/users/<int:userId>/watch_list/<int:securityId>': (users.delete_security_user_watchlist, ['DELETE']),
    '/v1/securities/search': (securities.search_securities, ['GET']),
    '/v1/login/': (auth.login, ['POST'])
}

"""
Route: /v1/users/<int:userId>/watch_list
Function: users.get_user_watch_list
HTTP Method: GET
Description: Retrieve the watchlist for a specific user.

Route: /v1/users/<int:userId>/watch_list/
Function: users.post_security_to_user_watchlist
HTTP Method: POST
Description: Add a security to a user's watchlist.

Route: /v1/users/<int:userId>/watch_list/<int:securityId>
Function: users.delete_security_user_watchlist
HTTP Method: DELETE
Description: Remove a security from a user's watchlist.

Route: /v1/securities/search
Function: securities.search_securities
HTTP Method: GET
Description: Search for securities based on specified criteria.

Route: /v1/securities/<int:securityId>
Function: securities.get_security_info
HTTP Method: GET
Description: Get information about a specific security.

Route: /v1/login/
Function: auth.login
HTTP Method: POST
Description: Perform user authentication and login.
"""