from operator import index
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()                     # FastAPI instance.

# This is a class to check the schema validation.
# It will validate the data it receives from the client for the title and content. 

class Post(BaseModel):
    title: str                      # Title should be string.
    content: str                    # Content should be string.
    published: bool = True          # by default it will evaluate to true.
    rating: Optional[int] = None    # This is a optional paramenter.
    

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
"title": "favorite foods", "content": "I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    
@app.get("/")
def read_root(): 
    return {"Hello": "Partha_Sarathi_Chakraborty"}

@app.get("/post")
def user_post():
    return {"Post": "This is your Partha Sarathi 0102"}

# Extract data from the body of the payload.
# Import the body using 'from fastapi.params import Body'.
# 'payload' is just a variable name and is a 'dict' type.
# returned a f"" [f-string].

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):      #Post is the class above.
    print(new_post)
    print(new_post.dict())            # Print the pydantic model to a dictionary.
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post detail": post}
    
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    # Deleting a post
    index = find_post_index(id)
    if index is not None and index != -1:
        my_posts.pop(index)
        return {"Message": "Post deleted successfully"}
    else:
        return {"Error": "Post not found"}


    
