from .. import models, schema, utils
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import FastAPI, HTTPException, status


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    #check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email {user.email} already exists")


    #hashed_password = pwd_context.hash(user.password)#this line hashes the password before storing it in the database.
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())#this line creates a new instance of the User model with the data from the user object.
    #The ** operator is used to unpack the dictionary returned by the user.dict() method and pass it as keyword arguments to the User constructor.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user