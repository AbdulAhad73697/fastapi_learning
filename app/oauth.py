from pyexpat import model
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status,Depends
from app.schemas import TokenData
from sqlalchemy.orm import Session
from app import database
from app import models
from app.config import settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   
    return encoded_jwt





def verify_access_token(token,
    credentials_exception ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
       
    except JWTError:
      raise credentials_exception
    return token_data
# this fuction for quering database
def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
   credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
   token_id = verify_access_token(token, credentials_exception)
   user = db.query(models.User).where(models.User.id == token_id.id ).first()
   
   return   user