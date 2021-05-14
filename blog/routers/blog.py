from typing import List
from fastapi import APIRouter,Depends,status,Response,HTTPException
from .. import schemas,database,models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
#Talvez possa remover o response das rotas...

get_db = database.get_db

router = APIRouter(
    tags=['Blogs']
)

@router.get('/blog',response_model=List[schemas.ShowBlog])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog,db : Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(jsonable_encoder(request))
    db.commit()
    return 'updated'
    
@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == 
                                        id).delete(synchronize_session=False)
    db.commit()
    return 'done'
    

@router.get('/blog/{id}',status_code=200,response_model = schemas.ShowBlog)
def show(id,response: Response,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detal':f"Blog with the id {id} is not available"}
    return blog
