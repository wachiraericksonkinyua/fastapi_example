from fastapi import APIRouter, Depends, HTTPException, status, Response ,Header
from sqlalchemy.orm import Session

from app.routers import user
from ..database import get_db
from .. import models, schema, utils ,auth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schema.Token)#user_credentials: OAuth2PasswordRequestForm = Depends()
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):#username: str = Header(...), password: str = Header(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == username).first()

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = auth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # if not utils.verify(password, user.password):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # #create a token and return it
    
    # access_token = auth2.create_access_token(data={"user_id": user.id})
    # return {"access_token": access_token, "token_type": "bearer"}

