from flask import Blueprint

blueprint = Blueprint('main', __name__)

@blueprint.route('/status')
def status():
    return 'OK'
