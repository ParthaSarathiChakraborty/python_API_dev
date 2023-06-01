# Path operations dealing with users.
from ..utils import hash_function
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# From the schema.py file.
from ..schema import CreateUser, UserOut

# from other file import statements
from ..database import get_db
from .. import models

router = APIRouter(
    prefix= "/users",
    # Improve the documentation readability by grouping them according to 'tags'.
    # Visit: 127.0.0.1:8000/redoc
    tags=["Users"]      
)

# This path operation creates a new user.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    
    # Hash the password: user.password
    # hash_function from the utils.py file.
    hashed_password = hash_function(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    # commit changes to the database.
    db.commit()
    # refresh the columns in the database.
    db.refresh(new_user)
    return new_user


# This path operation gets the details of a user using the user-id.
@router.get("/{id}", response_model=UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            details=f"User with id: {id} does not exist")
    return user

