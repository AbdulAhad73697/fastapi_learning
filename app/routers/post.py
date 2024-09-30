from pyexpat import model
from tkinter import S
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import func
from app.database import get_db
from app import models
from app.models import Post, Vote
from app.oauth import get_current_user
from app.schemas import PostCreate, PostResponse,PostOut,UserOut
from sqlalchemy.orm import Session

router = APIRouter(
   prefix="/posts",
   tags= ["Posts"], 
   
)


@router.get("/",response_model=list[PostOut])
def get_posts(db:Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 10, skip: int = 0, search: str | None = ""):
   print("Limit: ",limit)
   # print(current_user.id)
   print("Search: ", search)
   # posts =  db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
   results =(db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == Post.id, isouter=True ).group_by(Post.id)
             .filter(Post.title.contains(search)).limit(limit).offset(skip).all()
            )
   
   # print("Posts:  " , posts)
   # results = (
   #      db.query(Post, func.count(Vote.post_id).label("votes"))
   #      .outerjoin(Vote, Post.id == Vote.post_id)
   #      .filter(Post.title.contains(search))
   #      .group_by(Post.id)
   #      .limit(limit)
   #      .offset(skip)
   #      .all()
   #  )
   # # Return results using Pydantic's automatic conversion (thanks to orm_mode)
   return[
         {   
             "id": post.id,
             "title": post.title,
             "content": post.content,
             "published": post.published,
             "created_at": post.created_at,
             "owner_id": post.owner_id,
             "owner": post.owner,
             "votes": votes
            } for post, votes in results
            ]

@router.post("/", response_model=PostResponse)
async def create_posts(post:PostCreate, db:Session = Depends(get_db),current_user=Depends(get_current_user))->str:
  print("Current_User_ID: ", current_user.id)
  new_post = Post(owner_id=current_user.id ,**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


@router.get("/{id}",response_model=list[PostOut])
async def get_single_post(id: int, db:Session = Depends(get_db), current_user=Depends(get_current_user)):
   #  post= db.query(Post).filter(Post.id == id).first()
    results =(db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == Post.id, isouter=True ).group_by(Post.id)
              .filter (Post.id  == id)
              .all()
            )
    if not  results:
        raise HTTPException(status_code=404, detail="Gando ka bacha srif raise ke inder sa he la ga raise ka bara lora is ko pasand ha!")
   #  if post.owner_id != current_user.id:
   #     raise HTTPException(status_code=403, detail="Not Authorized to perform this action")
    
    return [
         {   
             "id": post.id,
             "title": post.title,
             "content": post.content,
             "published": post.published,
             "created_at": post.created_at,
             "owner_id": post.owner_id,
             "owner": post.owner,
             "votes": votes
            } for post, votes in results
           ]           


@router.delete("/{id}")
async def delete_post(id: int , db: Session = Depends(get_db),current_user=Depends(get_current_user) ):
   post_query = db.query(Post).filter(Post.id == id)
   post = post_query.first()
   if post == None:
      raise HTTPException(status_code=404, detail="Id not Found")
   if post.owner_id != current_user.id:
      raise HTTPException(status_code=403,detail="Not Authorized to perform required action")
   post_query.delete(synchronize_session=False)
   db.commit()
   return Response(status_code=204)   
        
      
@router.put("/{id}", response_model=PostResponse)
async def update_post(id: int ,post:PostCreate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
   post_query= db.query(Post).filter(Post.id == id)
   post_model = post_query.first()
   if post_model == None:
     raise HTTPException(status_code=404, detail="Id not found")
   
   if post_model.owner_id != current_user.id:
      raise HTTPException(status_code=403, detail="Not Authorized to Update")   
   
   post_query.update({**post.model_dump()}, synchronize_session=False)
   db.commit()
   return post_query.first()