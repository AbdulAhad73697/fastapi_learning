from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# from app.database import Base

class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    class Config:
        orm_mode = True
        
class PostCreate(PostBase):
     published: bool = True
     class Config:
        orm_mode = True

class UpdatePost(PostBase):
     published: bool
     class Config:
         orm_mode = True
class UserOut(BaseModel):
     id: int
     email: EmailStr
     created_at: datetime

     class Config:
        orm_mode = True

class PostResponse(PostBase):
     id: int
     created_at: datetime 
     owner_id: int
     owner:UserOut

     class Config:
        orm_mode = True   


         
    
class PostOut(BaseModel):
        id: int
        title: str
        content: str
        published: bool
        created_at: datetime
        owner_id: int
        owner: UserOut
        votes: int

        class Config:
          orm_mode = True

class UserCreate (BaseModel):
     email: EmailStr
     password: str
     class Config:
        orm_mode = True
     
class Token(BaseModel):
     access_token: str
     token_type: str
     class Config:
        orm_mode = True


class TokenData(BaseModel):
     id: str | None = None  
     class Config:
        orm_mode = True


class Vote(BaseModel):
     post_id: int
     # dir: conint(le=1)
     dir: int = Field(le=1,ge=0)
     class Config:
        orm_mode = True