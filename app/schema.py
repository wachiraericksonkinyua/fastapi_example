from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint
from pydantic import BaseModel, EmailStr, Field

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:#used to configure the behavior of the Pydantic model. In this case, it is used to specify that the model should be created from attributes of an object, rather than from a dictionary. This is useful when working with SQLAlchemy models, as it allows you to create Pydantic models directly from SQLAlchemy objects without having to convert them to dictionaries first.
        from_attributes = True

# This is the missing class your main.py is looking for!
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel): 
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    #dir : conint(le=1)
    dir: int = Field(le=1)

class PostOut(BaseModel):
    # This matches the Post model from models.py
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut
    # This is the new field for the count
    votes: int
    class Config:
        from_attributes = True