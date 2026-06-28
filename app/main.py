from typing import Optional
from random import randrange
from xml.parsers.expat import model
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from fastapi import Response , Depends
from httpx import get
from . import utils
from . import models
from .database import engine , SessionLocal , get_db
from sqlalchemy.orm import Session
from . import models , schema
from .routers import post, user, vote
from .routers import auth
from .config import settings

from fastapi.middleware.cors import CORSMiddleware
import os
from alembic.config import Config
from alembic import command
# models.Base.metadata.create_all(bind=engine)  # this line creates the tables in the database based on the models defined in the models.py file
# Run migrations automatically
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,#pasing a middleware
    allow_origins=origins,#what domains can talk to our api
    allow_credentials=True,#
    allow_methods=["*"],#can allow specific http methods
    allow_headers=["*"],#specific hederes
)


#storing our posts in the memory
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]



# def find_post(id): #here we are creating a function to find a post by its id
#     for p in my_posts:#iterating through the list of posts
#         if p['id'] == id:#checking if the id of the post matches the id we are looking for
#             return p

# def find_index_post(id): #here we are creating a function to find the index of a post by its id
#     for i, p in enumerate(my_posts):#iterating through the list of posts with an index
#         if p['id'] == id:#checking if the id of the post matches the id we are looking for
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
