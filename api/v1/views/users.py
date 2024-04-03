#!/usr/bin/python3
"""Hanldes index of pages and imports the blueprint"""

# import the blueprint
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


# Retrieves the list of all users of a User obj
@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def list_users():
    """lists all amenities"""
    # retrieve a dictionary of users
    users = storage.all(User).values()
    if users is None:
        abort(404)  # return 404 if None is returned
    users_json = [user.to_dict() for user in users]
    return jsonify(users_json), 200


# retrieve a userby ID
@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """fetches a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)  # return 404 if None is returned
    return jsonify(user.to_dict()), 200


# delete a user
@app_views.route('/user/<user_id>', methods=['GET'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a given user by id"""
    # get the specific user through id first
    user = storage.get(User, user_id)
    # check if user exists
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# creates a new User
@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """creates a new Amenity"""
    # transform the http body to a dictionary
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    # create a user instance based on data populated
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


# update a User
@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a user by ID"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    # update State object iwth all key-value pairs
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(User, key, value)
    user.save()
    # save the new object state
    return jsonify(user.to_dict()), 200
