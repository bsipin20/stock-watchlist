import logging
import sys
from datetime import datetime
from typing import List, Dict
from pytz import timezone
from typing import List, Dict, Optional
from dataclasses import dataclass
from flask import jsonify, request
from casestudy.services.security_service import create_security_service

@dataclass
class SearchRequest:
    query: str

    def validate(self):
        if len(self.query) < 3:
            raise ValueError("Query must be at least 3 characters long")

@dataclass
class Security:
    id: int
    ticker: str
    name: str
@dataclass
class SearchSecurityResponse:
    results: Optional[List[Security]]
    success: bool
    error: Optional[str]

def search_securities():
    query = request.args.get('query', '')
    search_request = SearchRequest(query)
    try:
        search_request.validate()
    except ValueError as e:
        return jsonify({'error': str(e)}), 422

    try:
        service = create_security_service()
        result = service.search_security(search_request.query)
        security_objects = []
        for security_data in result:
            security_obj = Security(id=security_data['id'], ticker=security_data['ticker'], name=security_data['name'])
            security_objects.append(security_obj)
        response = SearchSecurityResponse(results=security_objects, success=True, error=None)
        return jsonify(response), 200
    except (ValueError, TypeError, AttributeError) as e:
        logging.error(f'Error searching securities: {str(e)}')
        return jsonify({'error': "server error"}), 500


def get_security_info(securityId):
    service = create_security_service()
    security_info = service.get_security_info(securityId)
    return jsonify(security_info), 200
