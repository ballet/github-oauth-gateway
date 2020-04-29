from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import OperationalError


bcrypt = Bcrypt()


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object('ballet_oauth_gateway.conf.Config')

    if testing:
        app.config.from_object('ballet_oauth_gateway.conf.TestConfig')

    for key in app.config:
        print(f'{key}={app.config[key]}')

    from ballet_oauth_gateway.db import db
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except OperationalError:
            pass

    bcrypt.init_app(app)

    from ballet_oauth_gateway.api import blueprint
    app.register_blueprint(blueprint)

    return app
