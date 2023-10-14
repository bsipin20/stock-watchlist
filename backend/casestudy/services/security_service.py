import sys

from flask import jsonify, make_response
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional 

from casestudy.extensions import db, redis_client
from casestudy.database import Security

class SecurityDao:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

    def find_matching_securities_by_query(self, query):
         securities = self.db.session.query(Security).filter(
            (Security.name.ilike(f'%{query}%')) | (Security.ticker.ilike(f'%{query}%'))).all()
         return securities
    
    def get_latest_security_prices(self, securities):
        print(securities, file=sys.stderr)
        keys = [f'stock_info:{ticker}'.lower() for (ticker, ) in securities]
        result = []
        for key in keys:
            latest_security_price_info = self.redis_client.hgetall(key)
            if latest_security_price_info:
                parsed_info = {key.decode('utf-8'): value.decode('utf-8') for key, value in latest_security_price_info.items()}
                result.append(parsed_info)
        return result

class SecurityService:
    def __init__(self, security_dao):
        self.security_dao = security_dao

    def search_security(self, query):
        result = self.security_dao.find_matching_securities_by_query(query)
        if result:
            securities = [{'id': sec.id, 'ticker': sec.ticker, 'name': sec.name} for sec in result]
            return securities
        else:
            return []

def create_security_service():
    security_dao = SecurityDao(db, redis_client)
    return SecurityService(security_dao)
