import logging
import sys
from datetime import datetime
from pytz import timezone
from typing import List, Dict
from dataclasses import dataclass
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from pydantic import BaseModel

from casestudy.database import Security
from casestudy.extensions import db, redis_client
from casestudy.services.security_service import create_security_service

UTC_TIMEZONE = timezone('UTC')

def get_securities(securityId):
    security = Security.query.filter_by(id=securityId).first()
    security_dict = redis_client.hgetall(f'stock_info:{str(security.ticker).lower()}')
    decoded_data = {key.decode(): value.decode() for key, value in security_dict.items()}
    return { 'success': True, 'data': decoded_data }

def search_securities():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    if query == '':
        return jsonify([])
    else:
        service = create_security_service()
        result = service.search_security(query)
        if len(result) > 0:
            response = { 'results': { 'securities': result }, 'success': True }
            return jsonify(response), 200
        return jsonify([]), 200

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
