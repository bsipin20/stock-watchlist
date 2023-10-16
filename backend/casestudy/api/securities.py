"""
Module: securities.py

This module defines the methods related to securities
"""

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
    """
    Represents a search request with a query.

    Attributes:
    query (str): The search query string for the securities table.
    """
    query: str

    def validate(self):
        """
        Validates the search request.

        Raises:
        ValueError: If the query is less than 3 characters long.
        """
        if len(self.query) < 3:
            raise ValueError("Query must be at least 3 characters long")

@dataclass
class Security:
    """
    Represents security information.

    Attributes:
    id (int): The unique identifier for the security.
    ticker (str): The ticker symbol of the security.
    name (str): The name of the security.
    """
    id: int
    ticker: str
    name: str

@dataclass
class SearchSecurityResponse:
    """
    Represents the response for a security search.

    Attributes:
    results (Optional[List[Security]]): List of security objects matching the search.
    success (bool): Indicates if the search was successful.
    error (Optional[str]): Error message in case of an error.
    """
    results: Optional[List[Security]]
    success: bool
    error: Optional[str]

def search_securities():
    """
    Searches for securities based on the provided query.

    Returns:
    JSON response: A JSON response containing the search results.

    Raises:
    ValueError: If there is a validation error.
    """
    query = request.args.get('query', '')
    search_request = SearchRequest(query)
    try:
        search_request.validate()
    except ValueError as e:
        return jsonify({'error': "Query must be at least 3 characters"}), 422

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
        """ if the data from the api client changed typed or something """
        logging.error(f'Error searching securities: {str(e)}')
        return jsonify({'error': "server error"}), 500
