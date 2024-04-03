#!/usr/bin/python3
"""Hanldes index of pages and imports the blueprint"""

# import the blueprint
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


# Retrieves the list of all Amenities  obj of a State
@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def list_amenities():
    """lists all amenities"""
    # retrieve all a dictionary of amenities
    amenities = storage.all(Amenitity).values()
    if amenities is None:
        abort(404)  # return 404 if None is returned
    # fetch cities based on states
    amenities_json = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_json), 200


# retrieve an amenity by ID
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """fetches an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)  # return 404 if None is returned
    return jsonify(amenity.to_dict()), 200


# delete an amenity
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity given id"""
    amenity = storage.get(Amenity, amenity_id)
    # check if city exists
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# creates a new Amenity
@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creates a new Amenity"""
    # transform the http body to a dictionary
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    # create an amenity instance based on data populated
    amenity = Amount(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# update an Amenity
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    # update State object iwth all key-value pairs
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    # save the new object state
    return jsonify(amenity.to_dict()), 200
