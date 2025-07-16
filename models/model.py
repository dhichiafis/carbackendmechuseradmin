from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column('id',Integer,primary_key=True)
    username=Column('username',String,unique=True)
    password=Column('password',String)
    role=Column('role',String)
    profile=relationship('Profile',back_populates='user')
    reviews=relationship('Review',back_populates='user')
    
class Profile(Base):
    __tablename__='profiles'
    id=Column('id',Integer,primary_key=True)
    user_id=Column('user_id',Integer,ForeignKey('users.id'))
    email=Column('email',String,unique=True)
    user=relationship('User',back_populates='profile')
    
    
class Car(Base):
    __tablename__='cars'
    id=Column('id',Integer,primary_key=True)
    name=Column('name',String)
    image=Column('image',String)
    make=Column('make',String)
    bodytype=Column('bodytype',String)
    price=Column('price',Integer)
    specifications=relationship('Specifications',back_populates='car')
    gallery=relationship('Gallery',back_populates='car')
    reviews=relationship('Review',back_populates='car')
    
class Specifications(Base):
    __tablename__='specifications'
    id=Column('id',Integer,primary_key=True)
    car_id=Column('car_id',Integer,ForeignKey('cars.id'))
    mileage=Column('mileage',String)
    engine=Column('engine',String)
    drive=Column('drive',String)
    fuel=Column('fuel',String)
    steering=Column('steering',String)
    door=Column('door',Integer)
    seats=Column('seats',Integer)
    color=Column('color',String)
    car=relationship('Car',back_populates='specifications')
    
    
class Gallery(Base):
    __tablename__='gallery'
    id=Column('id',Integer,primary_key=True)
    carid=Column('carid',Integer,ForeignKey('cars.id'))
    image=Column('image',String)
    car=relationship('Car',back_populates='gallery')
    
class Review(Base):
    __tablename__='reviews'
    id=Column('id',Integer,primary_key=True)
    userreview=Column('userreview',Integer,ForeignKey('users.id'))
    carid=Column('carid',Integer,ForeignKey('cars.id'))
    rating=Column('rating',Integer)
    description=Column('description',String)
    car=relationship('Car',back_populates='reviews')
    user=relationship('User',back_populates='reviews')
    
    