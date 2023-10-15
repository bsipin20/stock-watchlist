import logging
import sys
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass
from flask import jsonify, request

from casestudy.services.security_service import create_security_service

def search_securities():
    """
    Flask route to search securities based on the 'query' parameter.

    Returns:
        JSON response containing the search results or an empty list.

    Example URL: /search?query=example_query
    Example Response:
    {
        "results": {
            "securities": [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "price": 145.12
                },
                {
                    "symbol": "GOOGL",
                    "name": "Alphabet Inc.",
                    "price": 2750.0
                }
            ]
        },
        "success": true
    }
    """
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
