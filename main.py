from typing import Optional
from fastapi import FastAPI
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

@app.post("/createpost")
def create_post(new_post: Post):      #Post is the class above.
    print(new_post)
    print(new_post.dict())            # Print the pydantic model to a dictionary.
    return {"data": new_post}

