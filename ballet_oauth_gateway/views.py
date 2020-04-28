from flask import Blueprint, current_app, jsonify, request

from ballet_oauth_gateway import db
from ballet_oauth_gateway.auth import request_token
from ballet_oauth_gateway.models import Auth

blueprint = Blueprint('main', __name__)


@blueprint.route('/status')
def status():
    return 'OK'


@blueprint.route('/api/app_id')
def app_id():
    return current_app.config['CLIENT_ID']


@blueprint.route('/api/authorize', methods=['GET'])
def authorize():
    """GitHub calls back here with code and copy of unique state"""
    # 1. get state and code from request
    code = request.args.get('code')
    state = request.args.get('state')

    # 2. insert to db
    auth = Auth(code=code, state=state)
    db.session.add(auth)
    db.session.commit()

    return 'OK'


@blueprint.route('/api/access_token', methods=['POST'])
def access_code():
    """User's client calls back here to request token"""
    # 1. get state from request
    state = request.form.get('state')

    # 2. get code from db
    auth = Auth.query.filter_by(state=state).first()
    code = auth.code

    # 3. request token from github
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET']
    redirect_uri = None  # TODO
    token_info = request_token(client_id, client_secret, code, redirect_uri, state)

    # 4. delete line from db
    db.session.delete(auth)
    db.session.commit()

    # 5. respond with token
    return jsonify(token_info)


@blueprint.route('/success', methods=['GET'])
def success():
    """User redirected here after authing with GitHub"""
    # TODO render template
    return 'You are successfully authorized'
