from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#used to hash the password before storing it in the database. 
# It uses the bcrypt algorithm to hash the password and automatically handles the salt and other parameters.

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

