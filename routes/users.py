from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from models.model import *
from models.schemas import *
from database import *
from fastapi.security import OAuth2PasswordRequestForm
from security import *

user_router=APIRouter(tags=['users'],prefix='/users')



@user_router.post('/new/user')
async def create_new_user(user:UserCreate,db:Session=Depends(connect)):
    user_db=db.query(User).filter(User.username==user.username).first()
    if user_db:
        raise HTTPException(detail='user already exiost '
                            ,status_code=status.HTTP_403_FORBIDDEN)
    password=get_password_hash(user.password)
    user_db=User(username=user.username,password=password,role=user.role)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db 

@user_router.post('/token')
async def create_login_access_token(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(connect)
):
    user=authenticate_user(form_data.username,form_data.password,db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect username or password',
            headers={"WWW-Authenticate":'Bearer'}
        )
    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(
        data={"sub":user.username,"role":user.role},expires_delta=access_token_expires
    )
    return Token(access_token=access_token,token_type='bearer')


@user_router.get('/all/users')
async def get_all_users(db:Session=Depends(connect)):
    return db.query(User).all()

@user_router.get('/users/me')
async def read_users_me(current:User=Depends(get_current_active_user)):
    return current 