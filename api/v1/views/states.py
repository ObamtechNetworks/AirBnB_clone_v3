#!/usr/bin/python3
"""Hanldes index of pages and imports the blueprint"""

# import the blueprint
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


# use to_dict() method to retrieve an object into a valid JSON
# Retrieves the list of all State objects
@app_views.route('/states/', methods=['GET'])
@app_views.route('/states', methods=['GET'])
def list_all_state():
    """lists all state object"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


# retireves a state object by id
@app_views.route('/states/<string:state_id>', methods=['GET'])
def state_by_id(state_id):
    """lists state by given id"""
    state = storage.get(State, state_id)
    # check if state exists
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


# deletes a state object
@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state_obj(state_id):
    """deletes a state"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# creates a new State
@app_views.route('/states', methods=['POST'])
def create_state():
    """creates a state obj"""
    # transform the http body to a dictionary
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    # unpack the data to create a new State instance
    new_state = State(**data)
    # save the new state
    new_state.save()
    # return the new created state with 201 response
    return jsonify(new_state.to_dict()), 201


# update a state
@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a state"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    # update State object iwth all key-value pairs
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    # save the new state
    state.save()
    return jsonify(state.to_dict()), 200
