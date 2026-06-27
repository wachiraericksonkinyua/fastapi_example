from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #relationship
    owner = relationship("User")


class User(Base):#this is the user model that will be used to create the users table in the database. It contains the following fields: id, email, password, created_at. The id field is the primary key and is auto-incremented. The email field is unique and cannot be null. The password field cannot be null. The created_at field is a timestamp that is automatically set to the current time when a new user is created.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
     __tablename__= "votes"

     user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"  ), primary_key=True)
     post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)