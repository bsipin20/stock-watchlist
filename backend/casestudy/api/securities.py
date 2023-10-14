import logging
import sys
from datetime import datetime
from pytz import timezone
from typing import List, Dict
from dataclasses import dataclass
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from pydantic import BaseModel, Optional, Any

from casestudy.database.models import Security
from casestudy.extensions import db, redis_client
from casestudy.app import get_or_create_redis_client, get_or_create_db_session
from casestudy.services.securities import SercuritiesService, UserWatchListService, SecurityDao

UTC_TIMEZONE = timezone('UTC')

class JsonResponse(BaseModel):
    results: Any
    success: bool
    error: Optional[str] = None
    message: Optional[str] = None

class SecurityGetResponse(JsonResponse):
    results: Optional[Security] = None

def get_securities(securityId):
    try:
        redis_client = get_or_create_redis_client()
        db = get_or_create_db_session()
        securities_service = SercuritiesService(SercurityDao(redis_client, db))
        result = securities_service.get_security_by_id(securityId)
        if result:
            result= SecurityGetResponse(results=response, success=True)
            return jsonify(response), 200
        else:
            result= SecurityGetResponse(results=None, success=False, error='Security not found')
            return jsonify(response), 404
    #TODO specific exceptions
    except Exception as e:
        logging.error(f'Error getting security: {e}')
        response = SecurityGetResponse(results=None, success=False, error='The server is currently unable to handle the request. Please try again later.')
        return jsonify(response), 500

class SearchSecuritiesResponse(JsonResponse):
    results: List[Optional[Security]] = []

def search_securities():
    try:
        query = request.args.get('query', '')
        if query == '' or len(query) < 3:
            response = SearchSecuritiesResponse(results=[], success=False, error='Query must be at least 3 characters')
            return jsonify(response.dict()), 400
        else:
            redis_client = get_or_create_redis_client()
            db = get_or_create_db_session()
            sercurities_service = SecuritiesService(SecurityDao(redis_client, db)
            result = sercurities_service.search_securities(query)
            if result:
                securities = [Security(id=sec.id, ticker=sec.ticker, name=sec.name) for sec in result]
                response = SecuritiesSearchResponse(results=securities, success=True)
                return jsonify(response.dict()), 200
            else:
                response = SecuritySearchResponse(results=[], success=True, message='No results found')
                return jsonify(response), 200
            return jsonify([])
    except Exception as e:
        logging.error(f'Error searching securities: {e}')
        response = SearchSecuritiesResponse(results=[], success=False, error= "The server is currently unable to handle the request. Please try again later.")
        return jsonify(response.dict()), 500
