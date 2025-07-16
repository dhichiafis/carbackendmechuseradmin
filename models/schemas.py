from pydantic import BaseModel
from typing import List

from enum import Enum 

class RoleType(str,Enum):
    admin='admin'
    mechanic='mechanic'
    user='user'
    
class UserCreate(BaseModel):
    username:str 
    password:str 
    role:RoleType
    

class UserBase(UserCreate):
    id:int 
    class Config:
        orm_mode=True
        
class ProfileCreat(BaseModel):
    
    email:str 
    
class ProfileBase(ProfileCreat):
    id:int 
    user_id:int #we dont know whose id we are creating the profile for but on retriveing we already know the user id
    class Config:
        orm_mode=True 
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class FuelType(str,Enum):
    PETROL='petrol'
    DIESEL='diesel'
    ELECTRIC='electric'       
 

class SpecificationsCreate(BaseModel):
    
    mileage:str
    engine:str 
    drive:str 
    fuel:FuelType
    steering:str 
    door:int 
    seats:int 
    color:str 
    
class SpecificationBase(SpecificationsCreate):
    id:int 
    car_id:int 
    class Config:
        orm_mode=True 
        
       
        
class CarCreate(BaseModel):
    name:str 
    make:str 
    image:str
    bodytype:str
    price:int 
    
class CarBase(CarCreate):
    id:int 
    specifications:List[SpecificationBase]
    class Config:
        orm_mode=True 

class GalleryCreate(BaseModel):
   
    image:str 
    
class GalleryBase(GalleryCreate):
    id:int 
    carid:int 
    class Config:
        orm_mode=True 
        
class ReviewCreate(BaseModel):
    
    rating:int 
    description:str 
    
    
class ReviewBase(ReviewCreate):
    id:int
    userreview:int 
    carid:int 
    class Config:
        orm_mode=True 
        