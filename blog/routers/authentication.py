from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..hashing import Hash
from .. import schemas, database,models  


router = APIRouter(
        tags = ['Authentication']
)

@router.post('/login')
def login(request:schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Password")
    #generate jwt token
    return user

