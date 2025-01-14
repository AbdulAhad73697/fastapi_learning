from turtle import st
from fastapi import FastAPI, APIRouter,Depends,HTTPException,Response,status
from app.schemas import Vote
from sqlalchemy.orm import Session
from .. import database, models,oauth

router = APIRouter(
    prefix="/vote",
    tags= ["Vote"]

)

@router.post("/", status_code=201)
def vote(vote:Vote, db:Session = Depends(database.get_db), current_user = Depends(oauth.get_current_user)):
    post = db.query(models.Vote).filter(models.Post.id == vote.post_id ).first()
    if not post :
        raise HTTPException(status_code=404, detail =f"Post with Id: {vote.post_id} doesnot exit")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir== 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote =  models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return{"message": "succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail = "Vote doesnot exist!")
        vote_query.delete(synchronize_session=False)    
        db.commit()
        return {"message": "successfully deleted vote"}