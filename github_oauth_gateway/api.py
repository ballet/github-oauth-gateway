from flask import Blueprint, current_app, request
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.exceptions import BadRequest

from github_oauth_gateway.auth import request_token
from github_oauth_gateway.db import db, Auth

blueprint = Blueprint('main', __name__)


@blueprint.route('/app_id')
def app_id():
    return {
        'client_id': current_app.config['CLIENT_ID'],
        'message': None,
    }


@blueprint.route('/authorize', methods=['GET'])
def authorize():
    """GitHub calls back here with code and copy of unique state"""
    # 1. get state and code from request
    try:
        code = request.args['code']
        state = request.args['state']
    except KeyError:
        raise BadRequest(description='Need to provide code and state params')

    # 2. delete any previous records for this state, as the rest of
    #    the oauth flow may have failed at the user's end
    db.session.query(Auth).filter_by(state=state).delete()

    # 3. insert to db
    auth = Auth(code=code, state=state)
    db.session.add(auth)
    db.session.commit()

    return {
        'message': 'OK',
    }


@blueprint.route('/access_token', methods=['POST'])
def access_code():
    """User's client calls back here to request token"""
    # 1. get state from request
    state = request.form.get('state')

    # 2. get code from db
    try:
        auth = Auth.query.filter_by(state=state).one()
        code = auth.code
    except (NoResultFound, MultipleResultsFound):
        raise BadRequest(description='No authorization code found for this state, may need to re-authenticate')

    # 3. request token from github
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET']
    redirect_uri = None  # TODO
    token_info = request_token(client_id, client_secret, code, redirect_uri, state)

    # 4. delete line from db
    db.session.delete(auth)
    db.session.commit()

    # 5. respond with token
    token_info['message'] = None
    return token_info


@blueprint.route('/success', methods=['GET'])
def success():
    """User redirected here after authing with GitHub"""
    # TODO render template
    return {
        'message': 'OK',
    }
