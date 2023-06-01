# This is the schema created from pydantic model.
from datetime import datetime
from pydantic import BaseModel, EmailStr
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True 

# Contains the schema for posts.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Schema for: update_post & create_post
class PostCreate(PostBase):
    pass

# This is the API response schema.
class PostResponse(PostBase):
    id: int
    
    # Already specified in the 'PostBase' class.
    # title: str
    # content: str
    # published: bool
    
    created_at: datetime

    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, 
    # but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True

# This is the schema to create an user.
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    

# Model to present the requested data to the user.
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # This is goint to be a sqlalchemy model. 
    # So convert it to pydantic.
    class Config:
        orm_mode = True 


# This schema will be used to get login info. from the user.

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    