from flask import Blueprint, current_app, jsonify, request

blueprint = Blueprint('main', __name__)


@blueprint.route('/status')
def status():
    return 'OK'


@blueprint.route('/app_id')
def app_id():
    return current_app.config['CLIENT_ID']


@blueprint.route('/authorize', methods=['GET'])
def authorize():
    """GitHub calls back here with code and copy of unique state"""
    code = request.args.get('code')
    state = request.args.get('state')
    print(f'code: {code}')
    print(f'state: {state}')
    return 'OK'


@blueprint.route('/access_code', methods=['POST'])
def access_code():
    """Users calls back here to request token"""
    state = request.form.get('state')
    # 1. get state from user
    # 2. get code from db
    # 3. request token from github
    # 4. delete line from db
    # 5. respond with token
    print(f'state: {state}')
    return jsonify({'Token': 'token'})


@blueprint.route('/success', methods=['GET'])
def success():
    """User redirected here after authing with GitHub"""
    return 'You are successfully authorized'
