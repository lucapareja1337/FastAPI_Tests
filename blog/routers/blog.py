from typing import List
from fastapi import APIRouter,Depends,status,Response,HTTPException
from .. import schemas,database,models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..repository import blog

#Talvez possa remover o response das rotas...

get_db = database.get_db

router = APIRouter(
    tags=['Blogs']
)

@router.get('/blog',response_model=List[schemas.ShowBlog])
def all(db : Session = Depends(get_db)):
    return blog.get_all(db)

@router.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog,db : Session = Depends(get_db)):
    return blog.create(request,db)


@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id,request,db)
    
    #
    
@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int,db : Session = Depends(get_db)):
    return blog.destroy(id,db)
    

@router.get('/blog/{id}',status_code=200,response_model = schemas.ShowBlog)
def show(id:int,response: Response,db : Session = Depends(get_db)):
   return blog.show(id,db)
