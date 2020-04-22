from flask import Flask

from ballet_oauth_gateway.views import blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(blueprint)

    return app
