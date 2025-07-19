from fastapi import FastAPI
import uvicorn 
from database import Base,engine
from routes.users import user_router
from routes.cars import cars_router
from routes.specifications import specs_router
from routes.profile import profile_router
Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user_router)
app.include_router(cars_router)
app.include_router(specs_router)
app.include_router(profile_router)

@app.get('/')
async def home(): 
    return {"message":'this is the homepage'}


#if __name__=="__main__":
    #uvicorn.run("main:app",reload=True,host='127.0.0.1',port=8000)