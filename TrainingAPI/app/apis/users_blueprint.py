import hashlib

import bcrypt
import json
from sanic import Blueprint, json

from app.databases.mongodb import MongoDB
from app.decorators.auth import protected
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiBadRequest, ApiInternalError, ApiNotFound
from app.models.user import user_json_schema, User
from sanic.response import json, text, raw

from app.utils.jwt_utils import generate_jwt

users_bp = Blueprint('users_blueprint', url_prefix='/users')
_db = MongoDB()


# bonus
@users_bp.route('/')
@protected
async def get_all_users(request, username=None):
    user_objs = _db.get_all_users()
    users = [user.to_dict() for user in user_objs]
    number_of_users = len(users)
    return json({
        'n_users': number_of_users,
        'users': users
    })


@users_bp.route('/register', methods={'POST'})
@validate_with_jsonschema(user_json_schema)
async def register_user(request):
    body = request.json
    user_name = body.get("username")
    pass_word = body.get("password")

    query = {"username": user_name}
    user = _db.get_user(query)
    if user:
        return json({'status': 'User has exited. Failed to register'})

    user_id = str(user_name)
    # user_password = str(bcrypt.hashpw(pass_word.encode('utf-8'), bcrypt.gensalt()))
    user_password = str(hashlib.sha256(pass_word.encode()).hexdigest())
    user_obj = User(user_id, user_name, user_password)
    user = _db.register_user(user_obj)
    if not user:
        raise ApiInternalError('Fail to register user')
    return json({'status': 'success'})


@users_bp.route("/login", methods=["POST", "GET"])
@validate_with_jsonschema(user_json_schema)
async def user_login(request):
    body = request.json
    user_name = body.get("username")
    pass_word = body.get("password")
    # user_password = str(bcrypt.hashpw(pass_word.encode('utf-8'), bcrypt.gensalt()))
    user_password = str(hashlib.sha256(pass_word.encode()).hexdigest())

    if (user_name is not None) and (pass_word is not None):
        query = {"username": user_name, "password": user_password}
        # query = {"username": user_name}
        user = _db.get_user(query)
        if not user:
            raise ApiNotFound("User does not exist or incorrect information")
    else:
        raise ApiBadRequest("Bad request")

    token_jwt = generate_jwt(user_name)

    return json({
        'status': "Login success",
        'token': token_jwt
    })


@users_bp.route('/logout', methods={'GET'})
@protected
async def user_logout(request, username=None):
    return json({'status': 'success'})
