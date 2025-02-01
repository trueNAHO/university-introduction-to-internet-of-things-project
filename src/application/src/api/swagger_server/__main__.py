#!/usr/bin/env python3

import connexion
from swagger_server import encoder

def main():
    # Create the connexion app instance
    app = connexion.App(__name__, specification_dir='./swagger/')

    # Get the Flask app instance from connexion
    flask_app = app.app

    # Set the JSON encoder
    flask_app.json_encoder = encoder.JSONEncoder

    # Add API with swagger.yaml
    app.add_api('swagger.yaml', arguments={'title': 'Project API'}, pythonic_params=True)

    # Run the application
    app.run(port=8087)

if __name__ == '__main__':
    main()

