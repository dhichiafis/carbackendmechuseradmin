import cloudinary.uploader
from fastapi import APIRouter,Depends,HTTPException,status,Form,UploadFile,File
from models.model import *
from models.schemas import *
from sqlalchemy.orm import Session 
from database import *
from security import *
from typing import List
import cloudinary
cars_router=APIRouter(tags=['cars'],prefix='/cars')

cloudinary.config(
    cloud_name="dxlvmhky1",
    api_key="946193632251344",
    api_secret="YaAPfX7YZgSPGxYoQi-pGJu07nI"
)
@cars_router.post('/new')
async def create_new_car(name:str=Form(...),make:str=Form(...),
    image:UploadFile=File(...),bodytype:str=Form(...),price:int=Form(...)
    ,user:User=Depends(Role_Checker(['admin']))
    ,db:Session=Depends(connect)):
    image=await image.read()
    image=cloudinary.uploader.upload(image)
    #my_car=Car(name=name,make=make,
    #           image=image,
    #           bodytype=bodytype,price=price)
    print(image['secure_url'])
    my_car=Car(name=name,make=make,image=image['secure_url']
               ,bodytype=bodytype,price=price)
    
    db.add(my_car)
    db.commit()
    db.refresh(my_car)
    return my_car


@cars_router.get('/all',response_model=List[CarBase])
async def all_cars(db:Session=Depends(connect),user:User=Depends(get_current_active_user)):
    return db.query(Car).all()

@cars_router.get('/{id}')
async def get_car(id:int,user:User=Depends(get_current_active_user)
                  ,db:Session=Depends(connect)):
    car=db.query(Car).filter(Car.id==id).first()
    if not car:
        raise HTTPException(detail="car with specified id does not exist",
                            status_code=status.HTTP_404_NOT_FOUND)
    return car 
