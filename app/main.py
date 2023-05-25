from typing import Optional
import time
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# This is the database connection.
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
        time.sleep(4)

@app.get("/")
def read_root():
    return {"Hello": "Partha_Sarathi_Chakraborty"}

# This block gets all the posts from the Postgre database.
@app.get("/post")
def user_post():
    cursor.execute("SELECT * FROM product")
    posts = cursor.fetchall()
    return {"Post": posts}

# This block creates a new post.

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute(
        "INSERT INTO product (title, content) VALUES (%s, %s) RETURNING *",
        (new_post.title, new_post.content),
    )
    post01 = cursor.fetchone()
    conn.commit()
    return {"data": post01}

# This block retrieves post with given 'id'.

@app.post("/posts/{id}")
def get_post(id: int):
    try:
        #The comma in this context is used to create a tuple with a single element (id,). 
        # It's a common syntax in Python to create a tuple with a single element. 
        cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
        # Fetch only one value.
        test_post = cursor.fetchone()
        print(test_post)
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



# This block of code deletes a single post with an 'id'

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    cursor.execute("DELETE FROM product WHERE id = %s", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    existing_post = cursor.fetchone()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    cursor.execute(
        "UPDATE product SET title = %s, content = %s, published = %s WHERE id = %s",
        (post.title, post.content, post.published, id)
    )
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)






