import os
import json
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = [os.environ['AUTH_ALGORITHM']]
API_AUDIENCE = os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
    it attempts to get the header from the request
    it raises an AuthError if no header is present
    it splits bearer and the token
    it raises an AuthError if the header is malformed
    if no error occurs it returns the token part of the header
    Source of the code snippet: Udacity Full Stack Nanodegree course
'''


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


# Permission check
'''
    function returns true if the payload contains the permission,
    posted via parameter "permission".
    it raises an AuthError if permissions are not included in the payload
    it raises an AuthError if the requested permission string is not
    in the payload permissions array
    Source of code snipped: Udacity Full Stack Developer Nanodegree
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'invalid_header',
            'description': '''You don't have the permission to
                            access the requested resource.'''
        }, 403)

    return True


'''
    Function to check whether the jwt is valid
    it verifies the token using Auth0 /.well-known/jwks.json
    it decodes the payload from the token
    it validates the claims
    and returns the decoded payload
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': '''Incorrect claims. Please, check
                                the audience and issuer.'''
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


# requires_auth decorator
'''
    it uses the get_token_auth_header method to get the token
    it uses the verify_decode_jwt method to decode the jwt
    it uses the check_permissions method validate claims and
    check the requested permission
    it returns the decorator which passes the decoded payload
    to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except BaseException:
                raise AuthError({
                    'code': 'Unauthorized',
                    'description': '''The server could not verify
                                    that you are authorized to
                                    access the URL requested.'''
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
