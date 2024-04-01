#!/usr/bin/python3
"""Begining to create my RESTAPI and route"""

from api.v1.views import app_views
from flask import Flask
import os
from models import storage

app = Flask(__name__)

# Register the blueprint
# Register with URL prefx
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_context(exception):
    """closes the storage connection on context teardown"""
    storage.close()


if __name__ == '__main__':
    # Use '0.0.0.0' if HBNB_API_HOST is not set
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    # Use 5000 if HBNB_API_PORT is not set
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the server with host, port, and threading
    app.run(host=host, port=port, threaded=True)
