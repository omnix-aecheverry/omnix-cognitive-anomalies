"""Module that contains the decorator for API Key authorization."""
import os
from functools import wraps
from flask import request

API_KEY = os.environ.get("API_KEY")

def verify_api_key(api_key):
    """Function that verifies the validity of the API Key token."""
    return api_key == API_KEY

def require_api_key(view_function):
    """Decorator that verifies the validity of the API Key token."""
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if "Authorization" in request.headers:
            api_key = request.headers["Authorization"].split()
            if len(api_key) == 2:
                api_key = api_key[1]
            else:
                api_key = api_key[0]
            if verify_api_key(api_key):
                return view_function(*args, **kwargs)
        return { "message": "Unauthorized" }, 401
    return decorated_function