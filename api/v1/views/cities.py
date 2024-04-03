#!/usr/bin/python3
"""Hanldes index of pages and imports the blueprint"""

# import the blueprint
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


# Retrieves the list of all City obj of a State
@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def list_all_cities(state_id):
    """lists all cities of a state"""
    # retrieve all states first
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # return 404 if None is returned
    # fetch cities based on states
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# retireves a city obj by id
@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_by_id(city_id):
    """fetch city by given id"""
    city = storage.get(City, city_id)
    # check if city exists
    if not city:
        abort(404)
    return jsonify(state.to_dict()), 200


# deletes a city object
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_obj(city_id):
    """deletes a city obj by id"""
    city = storage.get(City, state_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


# creates a new State
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city for a state"""
    # get a state by the given id
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # transform the http body to a dictionary
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


# update a city
@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a state"""
    city = storage.get(City, state_id)

    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    # update State object iwth all key-value pairs
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    # save the new state
    return jsonify(city.to_dict()), 200
