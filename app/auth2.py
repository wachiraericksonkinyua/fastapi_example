from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from . import schema, database, models
from app import schema
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")#this line creates an instance of the OAuth2PasswordBearer class, which is used to handle the authentication process. The tokenUrl parameter specifies the endpoint where the user can obtain a token by providing their credentials. In this case, the endpoint is set to "login", which corresponds to the login route defined in the auth router.
#what we provide about the token:
#secret key, algorithm, expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME_MINUTES = settings.access_token_expire_time

def create_access_token(data: dict):
    to_encode = data.copy()#this line creates a copy of the data dictionary that is passed as an argument to the function. This is done to avoid modifying the original data dictionary.
    expire = datetime.utcnow() + timedelta(minutes=int(EXPIRATION_TIME_MINUTES))
    to_encode.update({"exp": expire})#this line adds the expiration time to the data
    encode_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)#this line encodes the data dictionary into a JWT token using the secret key and algorithm specified in the constants. The result is a string that represents the encoded JWT token.
    return encode_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])#this line decodes the JWT token using the secret key and algorithm specified in the constants. The result is a dictionary that contains the data that was encoded in the token.
    except JWTError:
        raise credentials_exception

    id = payload.get("user_id")#this line retrieves the user_id from the decoded payload. If the user_id is not present in the payload, it will return None.
    if id is None:
        raise credentials_exception

    token_data = schema.TokenData(id=id)#this line creates an instance of the TokenData class from the schema module, passing the user_id as an argument. This instance will be used to return the user_id to the caller.
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()#this line queries the database for a user with the id that was extracted from the token. If a user is found, it will be returned. If no user is found, it will return None.
    return user
