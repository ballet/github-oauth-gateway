from werkzeug.exceptions import BadRequest, InternalServerError


class NoAuthCode(BadRequest):
    description = 'No authorization code found for this state, may need to re-authenticate'


class MultipleAuthCodes(InternalServerError):
    description='unexpectedly found multiple codes for this state, try auth flow from beginning'


class AuthTokenExchangeDenied(BadRequest):
    description='Authorization token denied'
