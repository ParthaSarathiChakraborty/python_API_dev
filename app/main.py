from multiprocessing import synchronize
from turtle import title
from typing import Optional
import time
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .schema import PostCreate
# from other file import statements
from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

# This is the fastAPI instance.
app = FastAPI()

# This is the database connection. Uses try-except block.
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='parthasarathichakraborty',
            password='',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Connection Successful")
        break
    except Exception as error:
        print("Connection Failed.")
        print("Error: ", error)
        # Checks for connection for every 4 sec.
        time.sleep(4)

@app.get("/")
def read_root():
    return {"Hello": "Partha_Sarathi_Chakraborty"}

# imports the get_db method from the models.py file.
# '/sqlalchemy' is an API specific route.

# @app.get("/sqlalchemy")
# # Dependency.
# # db is a session.
# def testing_post(db: Session = Depends(get_db)):
#     # Create a session call. 
#     posts = db.query(models.Post).all()
#     return {"data": posts}

 
# This block gets all the posts from the Postgre database.
@app.get("/post")
def user_post():
    cursor.execute("SELECT * FROM product")
    posts = cursor.fetchall()
    return {"Post": posts}


# This block creates a new post.
# payload in postman 'raw' section using json.

@app.post("/post", status_code=status.HTTP_201_CREATED)
# Function to create post using ORM. This is the database connection call.
def create_post(new_post: PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute(
    #     "INSERT INTO product (title, content) VALUES (%s, %s) RETURNING *",
    #     (new_post.title, new_post.content),
    # )
    # post01 = cursor.fetchone()
    # conn.commit()
    
    # unpack the dictionary to match the schema automatically.
    # print(**new_post.dict())
    
    post01 = models.Post(**new_post.dict())
    db.add(post01)
    # commit changes to the database.
    db.commit()
    # refresh the columns in the database.
    db.refresh(post01)
    return {"data": post01}


# This block retrieves post with given 'id'.

@app.get("/posts/{id}")
# The database dependency.
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        #The , in this context is used to create a tuple with a single element (id,). 
        # It's a common syntax in Python to create a tuple with a single element. 
        
        # cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
        # Fetch only one value.
        # test_post = cursor.fetchone()
        
        test_post = db.query(models.Post).filter(models.Post.id == id).first()
        # print(test_post)
        # Raise the HTTP EXCEPTION ERROR.
        if not test_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} was not found"
            )
        return test_post
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of an error
        raise e  # Re-raise the exception to be handled by FastAPI


# In the context of database transactions, a rollback is an operation that undoes or cancels the changes made within a transaction. It restores the database to its previous state before the transaction began.

# When working with a database, changes are typically grouped into transactions. A transaction is a logical unit of work that may consist of multiple database operations, such as inserting, updating, or deleting records. These operations are executed as a single unit, and the changes are committed to the database when the transaction is completed successfully.

# However, there are situations where a transaction may encounter an error or fail to complete successfully. In such cases, a rollback is performed to undo the changes made within the transaction. The database is reverted to the state it was in before the transaction started, ensuring data consistency and integrity.

# Rollbacks are essential for maintaining data integrity and handling error conditions in database operations. They provide a way to recover from failures and ensure that changes are not permanently applied to the database when an error occurs.

# In the context of the code you shared, the rollback can be used in the exception handling block when an error occurs during the execution of SQL statements. It ensures that any changes made within the transaction are rolled back if an exception is raised, preventing incomplete or inconsistent data from being stored in the database.



# This block of code 'delete' a single post with an 'id'
# This is a delete operation.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# The database dependency into the path operation function.
def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    # deleted_post = cursor.fetchone()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    deleted_post.delete(synchronize_session = False)
    
    # cursor.execute("DELETE FROM product WHERE id = %s", (id,))
    
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# This code block updates a single post with the given 'ID'.


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    # existing_post = cursor.fetchone()
    
    post_query = db. query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    # if not post.title:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")

    # if not post.content:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content is required")

    # cursor.execute(
    #     "UPDATE product SET title = %s, content = %s, published = %s WHERE id = %s",
    #     (post.title, post.content, post.published, id))
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
