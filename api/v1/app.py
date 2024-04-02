#!/usr/bin/python3
"""
A module to create my RESTAPIFUL and route
"""


import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register the blueprint
# Register with URL prefx
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_context(exception):
    """closes the storage connection on context teardown"""
    storage.close()


@app.errorhandler(404)
def custom_404(error):
    """Returns a custom 404 response message"""
    resp = jsonify({"error": "Not found"})
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    # Use '0.0.0.0' if HBNB_API_HOST is not set
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    # Use 5000 if HBNB_API_PORT is not set
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the server with host, port, and threading
    app.run(host=host, port=port, threaded=True)
