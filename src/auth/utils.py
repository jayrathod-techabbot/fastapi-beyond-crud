from passlib.context import CryptContext
import jwt
from datetime import timedelta,datetime
from src.config import Config
import uuid
import logging

ACCESS_TOKEN_EXPIRE = 3600

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_data: dict ,expiry : timedelta=None, refresh :bool =False) -> str:
    payload = { }
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRE))
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET,
        algorithm = Config.JWT_ALGORITHM
    )
    return token

def decode_access_token(token:str) -> dict : 
    try:
        token_data = jwt.decode(
            token,
            Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
