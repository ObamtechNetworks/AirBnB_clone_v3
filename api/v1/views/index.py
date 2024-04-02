#!/usr/bin/python3
"""Hanldes index of pages and imports the blueprint"""

# import the blueprint
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Returns a JSON response indicating the application status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def fetch_stats():
    """Fetches the number of each object by type"""
    model_stats = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(model_stats)
