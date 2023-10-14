import sys

from flask import jsonify, make_response
from casestudy.database.dao import SecurityDao

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
