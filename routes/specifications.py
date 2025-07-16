from fastapi import APIRouter,Depends,HTTPException,status
from models.model import *
from models.schemas import *
from sqlalchemy.orm import Session 
from database import *
from security import *
specs_router=APIRouter(tags=['specs'],prefix='/specs')


@specs_router.post('/new/cars/{id}')
async def create_car_specs(
    id:int,
    new_specs:SpecificationsCreate,
    user:User=Depends(Role_Checker(['admin']))
    ,db:Session=Depends(connect)):
    car=db.query(Car).filter(Car.id==id).first()
    my_car=Specifications(mileage=new_specs.mileage,
                          engine=new_specs.engine,
    drive=new_specs.drive,
    fuel=new_specs.fuel,
    steering=new_specs.steering,
    door=new_specs.door,
    seats=new_specs.seats,
    color=new_specs.color
                        )
    my_car.car_id=car.id
    db.add(my_car)
    db.commit()
    db.refresh(my_car)
    return my_car


