# This file contains the authentication.

import email
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from ..database import get_db
from ..schema import UserLogin
from ..models import *
from .. import utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

# Create the login path operation.
@router.post("/login")
@router.post("/login")
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user_info = db.query(User).filter(User.email == user_cred.username).first()
    
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
     
    if not utils.verify(user_cred.password, user_info.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user_info.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


    