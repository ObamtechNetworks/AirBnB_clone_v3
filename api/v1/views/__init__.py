#!/usr/bin/python3
"""handles views and blueprint"""

from flask import Blueprint


app_views = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# improt all views from this package
from . import index
