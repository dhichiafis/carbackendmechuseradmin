from datetime import datetime,timedelta,timezone
from models.schemas import *
from models.model import *
from jose import jwt,JWTError
from typing import List
from fastapi import Depends,HTTPException,status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext

from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import *

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username:str,db:Session):
    return db.query(User).filter(User.username==username).first()


def authenticate_user(username: str, password: str,db:Session):
    user = get_user(username,db=db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str=Depends(oauth2_scheme),
                           db:Session=Depends(connect)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username,db=db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user:User=Depends(get_current_user),
):
    
    return current_user


def Role_Checker(allowed_roles:List[str]):
    def checker(user:User=Depends(get_current_active_user)):
        if user.role not in allowed_roles:
            raise HTTPException(detail='user has no permissions'
                                ,status_code=status.HTTP_401_UNAUTHORIZED)
        return user 
    return checker