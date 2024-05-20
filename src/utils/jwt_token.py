import jwt
from datetime import timedelta, datetime
from config import Config

def generate_jwt_tokens(payload: dict) -> dict:
    # Define expiration times for access and refresh tokens
    access_token_exp = datetime.utcnow() + timedelta(minutes=60)
    refresh_token_exp = datetime.utcnow() + timedelta(days=7)

    # Create access token
    access_token_payload = payload.copy()
    access_token_payload["exp"] = access_token_exp
    access_token = jwt.encode(
        payload=access_token_payload, key=Config.JWT_SECRET_KEY, algorithm="HS256"
    )

    # Create refresh token
    refresh_token_payload = payload.copy()
    refresh_token_payload["exp"] = refresh_token_exp
    refresh_token = jwt.encode(
        payload=refresh_token_payload,
        key=Config.JWT_REFRESH_SECRET_KEY,
        algorithm="HS256",
    )
    return {"access_token": access_token, "refresh_token": refresh_token}
