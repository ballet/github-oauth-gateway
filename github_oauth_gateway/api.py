import time

from flask import Blueprint, current_app, request
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.exceptions import BadRequest, InternalServerError

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
    content = request.get_json(force=True)
    state = content['state']
    timeout = content.get('timeout', current_app.config['ACCESS_CODE_TIMEOUT'])
    interval = current_app.config['ACCESS_CODE_POLL_INTERVAL']
    start = time.time()

    # 2. get code from db, waiting if necessary
    while True:
        try:
            auth = db.session.query(Auth).filter_by(state=state).one()
            code = auth.code
            break
        except NoResultFound:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise BadRequest(description='No authorization code found for this state, may need to re-authenticate')
            else:
                sleep_time = min(interval, timeout - elapsed)
                current_app.logger.info(
                    f'Didn\'t find state, will sleep for {sleep_time} seconds ({timeout - elapsed} remaining)')
                time.sleep(sleep_time)
                continue
        except MultipleResultsFound:
            try:
                db.session.query(Auth).filter_by(state=state).delete()
                db.session.commit()
            finally:
                raise InternalServerError(
                    description='unexpectedly found multiple codes for this state, try auth flow from beginning')

    # 3. request token from github
    client_id = current_app.config['CLIENT_ID']
    client_secret = current_app.config['CLIENT_SECRET']
    redirect_uri = None  # TODO
    token_info = request_token(client_id, client_secret, code, redirect_uri, state)

    # github may include error code in body
    if 'error' in token_info and token_info['error']:
        current_app.logger.exception('got error response from GitHub: {token_info}')
        raise BadRequest(description='Authorization token denied')

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
