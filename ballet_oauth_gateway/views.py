from flask import Blueprint, request

blueprint = Blueprint('main', __name__)


@blueprint.route('/status')
def status():
    return 'OK'


@blueprint.route('/app_id')
def app_id():
    return 0


@blueprint.route('/authorize')
def authorize():
    code = request.args.get('code')
    state = request.args.get('state')
    print(f'code: {code}')
    print(f'state: {state}')


@blueprint.route('/access_code', methods=['POST'])
def access_code():
    state = request.form.get('state')
    print(f'state: {state}')
