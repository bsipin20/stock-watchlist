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
