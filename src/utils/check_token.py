from flask import g, request
import jwt
from src.database import db
from config import Config
from src.models.user import User
from functools import wraps


def login_required(func):
    @wraps(func)
    def inner(*args, **kwrgs):
        try:
            if not 'Authorization' in request.headers:
                return {'error':'Token not found'}, 401
            token = request.headers.get('Authorization').split()[1]
            decoded_token_detail = jwt.decode(token, key=Config.JWT_SECRET_KEY, algorithms='HS256')

            user_id = decoded_token_detail.get('user_id')
            user = db.session.query(User).get(user_id)
            if not user:
                return {'error':'user not found'}, 404
            g.user = user
            return func(*args, **kwrgs)
        except Exception as e:
            return {'error':str(e)}
    return inner

