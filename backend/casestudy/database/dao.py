
"""
This a DAO class for User 
the idea behind using a DAO is to separate the database logic from the business logic
We don't want services to be concerned with how the data is stored in the database
This implementation uses redis but the service shouldnt' care if its redis, postgres, timeseries db, nosql, etc
"""
import logging
from redis.exceptions import RedisConnectionError
from database import redis_client

class UserDao:
    def get_user_by_id(self, user_id):
        pass

class SecurityPriceDao:
    def get_latest_security_prices(self, ticker_symbols):
        try:
            keys = [f'stock_info:{ticker}'.lower() for (ticker, ) in ticker_symbols]
            response = []
            for redis_key in keys:
                security_dict = redis_client.hgetall(redis_key)
                if security_dict:
                    security_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in security_dict.items()}
                    response.append(security_dict)
            return response
        except RedisConnectionError:
            logging.error(f'Failed to connect to Redis')
            return False



