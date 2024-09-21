from flask import Flask
from flask_cors import CORS
from serving.controller.deployment_controller import deployment_bp


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS to avoid browser blocking cross-origin requests

    # Register the blueprint for deployments
    app.register_blueprint(deployment_bp, url_prefix="/api/deployments")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=1409)
