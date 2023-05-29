# This is the schema created from pydantic model.
from pydantic import BaseModel

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True 

# Contains the schema for posts 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True    


# Schema for: update_post & create_post

class PostCreate(PostBase):
    pass
