# Path operations dealing with posts.
 
from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# From the schema.py file.
from ..schema import PostCreate, PostResponse

# from other file import statements
from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/post",
    # Improve the documentation readability by grouping them according to tags.
    tags=["Posts"]                      
)

# This block gets all the posts from the Postgre database.
@router.get("/", response_model= List[PostResponse])   # Change 'PostResponse' to a List[].
def user_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()                 # Get all the data using .all()
    return posts

# This block creates a new post.
# payload in postman 'raw' section using json.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= PostResponse)
# Function to create post using ORM. This is the database connection call.
def create_post(new_post: PostCreate, db: Session = Depends(get_db)):    
    post01 = models.Post(**new_post.dict())
    
    db.add(post01)
    # commit changes to the database.
    db.commit()
    # refresh the columns in the database.
    db.refresh(post01)
    return post01


# This block retrieves post with given 'id'.
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model= PostResponse)
# The database dependency.
def get_post(id: int, db: Session = Depends(get_db)):
    try:        
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
        db.rollback()    # Rollback the transaction in case of an error
        raise e          # Re-raise the exception to be handled by FastAPI


# In the context of database transactions, a rollback is an operation that undoes or cancels the changes made within a transaction. It restores the database to its previous state before the transaction began.

# When working with a database, changes are typically grouped into transactions. A transaction is a logical unit of work that may consist of multiple database operations, such as inserting, updating, or deleting records. These operations are executed as a single unit, and the changes are committed to the database when the transaction is completed successfully.

# However, there are situations where a transaction may encounter an error or fail to complete successfully. In such cases, a rollback is performed to undo the changes made within the transaction. The database is reverted to the state it was in before the transaction started, ensuring data consistency and integrity.

# Rollbacks are essential for maintaining data integrity and handling error conditions in database operations. They provide a way to recover from failures and ensure that changes are not permanently applied to the database when an error occurs.

# In the context of the code you shared, the rollback can be used in the exception handling block when an error occurs during the execution of SQL statements. It ensures that any changes made within the transaction are rolled back if an exception is raised, preventing incomplete or inconsistent data from being stored in the database.



# This block of code 'delete' a single post with an 'id'
# This is a 'DEL' operation.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    db.delete(deleted_post)
    db.commit()


# This code block updates a single post with the given 'ID'.
@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # This is the exception block.
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
