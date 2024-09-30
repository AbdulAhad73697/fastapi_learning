from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.utils import get_password_hash
from sqlalchemy.orm import Session

router = APIRouter(
   prefix="/users",
   tags= ["Users"]
)


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=UserOut)
async def create_user( user:UserCreate , db:Session = Depends(get_db)):
   hashed_password = get_password_hash(user.password)
   user.password = hashed_password
   new_user = User(**user.model_dump())
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user

@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
   user = db.query(User).filter(User.id == id).first()
   if not user:
      raise HTTPException(status_code=404, detail="Gando ka bacha srif raise ke inder sa he la ga raise ka bara lora is ko pasand ha!")
   return user
