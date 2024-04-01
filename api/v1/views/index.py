#!/usr/bin/python3
"""Hanldes index of pages and imports the blueprint"""

# import the blueprint
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns a JSON response indicating the application status"""
    return jsonify({'status': 'OK'})
