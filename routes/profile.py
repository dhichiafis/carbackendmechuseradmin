from fastapi import APIRouter,Depends,status,UploadFile,File
from models.model import Profile,User
from models.schemas import ProfileBase,ProfileCreat
from security import *

from database import connect

from sqlalchemy.orm import Session


profile_router=APIRouter(tags=['profiles'],prefix='/profile')
@profile_router.post('/new/',response_model=ProfileBase)
async def create_new_profile(
    profile:ProfileCreat,
    user:User=Depends(get_current_active_user) ,
    db:Session=Depends(connect)    
                             ):
    
    profile=Profile(**profile.dict())
    profile.user_id=user.id
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@profile_router.get('/all')
async def get_all_profiles(db:Session=Depends(connect),user:User=Depends(Role_Checker(['admin']))):
    return db.query(Profile).all()


