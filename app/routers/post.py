from .. import models, schema, auth2
from fastapi import APIRouter, Depends, HTTPException, Response, status , Query 
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List , Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/")
# async def root():
#     return {"message": "Hello to my Api"}

# @router.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):#this line is a dependency that allows us to get a database session that we can use to interact with the database. It uses the get_db function defined in the database.py file to create a new session and automatically close it after the request is finished.
#     # posts = db.query(models.Post).all()
#     #posts = db.query(models.Post).filter(models.Post.id == 1).first()
#     posts= db.query(models.Post).all()
#     return {"status": "success", "data": posts}

# @router.get("/", response_model=list[schema.Post], status_code=status.HTTP_200_OK)
# async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user), limit : int = 10, skip : int =0 ,search: Optional[str]= ""):#this line is a dependency that allows us to get a database session that we can use to interact with the database. It uses the get_db function defined in the database.py file to create a new session and automatically close it after the request is finished.
#     print(limit)
#     # cursor.execute("""SELECT * FROM posts""")#this line executes a SQL query to select all posts from the database
#     # posts = cursor.fetchall()#this line fetches all the results of the query and stores them in the posts variable
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     print(posts)
#     return posts
# routers/post.py
# @router.get("/", response_model=list[schema.PostOut])
# async def get_posts(db: Session = Depends(get_db)):
#     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
#         models.Vote, models.Vote.post_id == models.Post.id, isouter=True ).group_by(models.Post.id).all() 
#     # Format the result to return the Post object and the votes count
#     # routers/post.py - Revised get_posts loop
#     posts = []
#     for post, votes in results:
#         # Create a dictionary that explicitly includes the owner object and the votes count
#         post_item = {
#             "id": post.id,
#             "title": post.title,
#             "content": post.content,
#             "published": post.published,
#             "created_at": post.created_at,
#             "owner_id": post.owner_id,
#             "owner": post.owner, # This must be the User object from the relationship
#             "votes": votes
#         }
#         posts.append(post_item)
#     return posts

@router.get("/", response_model=list[schema.PostOut])
async def get_posts(db: Session = Depends(get_db)):
    # We use join and group_by, but keep the SQLAlchemy object intact
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).all()
    
    posts_list = []
    for post, votes in results:
        # Instead of manual dict, we construct an object that matches schema.PostOut
        post_data = schema.PostOut(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner_id=post.owner_id,
            owner=post.owner, # SQLAlchemy handles the relationship here
            votes=votes
        )
        posts_list.append(post_data)
    return posts_list
#we want user to send us a json with title string and content string
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post, )#decorator to create a post
async def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):#demands that incoming info match the rules of your post pydantic model
    # post_dict = new_post.dict()#It transforms the validated object into a plain, easy-to-use Python dictionary.
    # post_dict['id'] = randrange(0, 1000000)#slaps a randomly generated number onto your new dictionary
    # my_posts.append(post_dict)#This line literally stuffs your freshly stamped dictionary right into the my_posts list to keep it safe.
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (new_post.title, new_post.content, new_post.published))#this line executes a SQL query to insert a new post into the database and returns the newly created post
    # new_postpost = cursor.fetchone()#this line fetches the newly created post and stores it in the post variable
    # conn.commit()#this line commits the changes to the database
    print(current_user.id)#this line prints the validated data from the new_post object as a dictionary
    #print(current_user.email)#this line prints the validated data from the new_post object as a dictionary
    new_postpost = models.Post(owner_id=current_user.id, **new_post.dict())#title=new_post.title, content=new_post.content, published=new_post.published, owner_id=current_user.id)#this line creates a new instance of the Post model with the data from the new_post object
    db.add(new_postpost)
    db.commit()
    db.refresh(new_postpost)
    return new_postpost#It happily hands the finalized post data straight back to whoever made the request.

#retrieving one post
@router.get("/{id}", response_model=schema.Post)#decorator to retrieve a post
async def get_post(id: int , response: Response, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):#:int will automatically convert the incoming string to an integer
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))#this line executes a SQL query to select a post by its id from the database
    # test_post = cursor.fetchone()
    # 1. Fetch the specific post by its ID
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # 2. Check if the post actually exists first
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    # 3. Check if the current user is the owner
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # 4. Return the post if everything is good!
    return post
# #dummy route 
# @router.get("/posts/latest")#decorator to retrieve a post
# async def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return post

#deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    #find the index in the list that matches the id
    #my_posts.pop(index) to remove it from the list
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))#
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db.delete(deleted_post)
    db.commit()
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#updating a post
@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth2.get_current_user)):
    
    # 1. Prepare the query and fetch the target post
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = updated_post_query.first()
    
    # 2. Check if the post even exists
    if post_to_update == None:#this
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    # 3. SECURITY CHECK: Does the current user own this post?
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # 4. Save the new changes safely
    updated_post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return updated_post_query.first()