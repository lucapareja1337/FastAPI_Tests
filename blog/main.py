
from typing import List
from fastapi import FastAPI
from . import models
from .hashing import Hash
#from fastapi.encoders import jsonable_encoder
from .database import engine,get_db
from .routers import blog,user
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router) 

app.include_router(user.router) 

