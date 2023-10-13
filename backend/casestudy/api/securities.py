import logging
from datetime import datetime
from pytz import timezone
from typing import List, Dict
from dataclasses import dataclass
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from pydantic import BaseModel

from casestudy.database import Security
from casestudy.extensions import db, redis

UTC_TIMEZONE = timezone('UTC')

def get_securities(securityId):
    security = Security.query.filter_by(id=securityId).first()
    security_dict = redis_client.hgetall(f'stock_info:{security.ticker}')
    return { 'success': True, 'data': security_dict }

def search_securities():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    if query == '':
        return jsonify([])
    else:
        result = _find_matching_securities(query)
        if result:
            #TODO replace with pydantic validator
            response = { 'results': { 'securities': result }, 'success': True }
            print(response)
            return jsonify(response)
        return jsonify([])

def _find_matching_securities(query):
    securities = db.session.query(Security).filter(
        (Security.name.ilike(f'%{query}%')) | (Security.ticker.ilike(f'%{query}%'))
    ).all()
    return securities

@dataclass
class SecurityDTO:
    id: int
    ticker: str
    name: str

class SecuritySearchResponse(BaseModel):
    results: Dict[str, List[SecurityDTO]]
    success: bool
    error: str = None

def search_securities():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    if query == '':
        repsonse = SecuritySearchResponse(results=[], success=True) 
        return jsonify(repsonse.dict()), 200
    else:
        result = _find_matching_securities(query)
        if result:
            securities = [SecurityDTO(id=sec.id, ticker=sec.ticker, name=sec.name) for sec in result]
            response = SecuritySearchResponse(results={'securities': securities}, success=True)
            return jsonify(response.dict())
        return jsonify([])
