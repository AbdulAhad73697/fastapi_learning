from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import verify_password
from app.oauth import  create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import Token
router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
async def login(
    form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)
) -> Token:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
      raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
      
    access_token = create_access_token(
        data={"user_id": str(user.id)}
    )
    
    return Token(access_token=access_token, token_type="bearer")
