from .. import models, schema, utils ,database , auth2
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import FastAPI, HTTPException, status

router= APIRouter(
    prefix="/vote",
    tags = ['vote']
)

# In app/routers/vote.py

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(auth2.get_current_user)):
    
    # 1. Verify the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    # 2. Proceed with vote logic
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first() 
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(auth2.get_current_user)):
#     vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
#     found_vote = vote_query.first() 
    
#     if (vote.dir == 1):
#         if found_vote:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
#         new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
#         db.add(new_vote)
#         db.commit()
#         return {"message": "successfully added vote"} # <--- ADD THIS
        
#     else:
#         if not found_vote:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
#         vote_query.delete(synchronize_session=False)
#         db.commit()
#         return {"message": "successfully deleted vote"}