from multiprocessing import AuthenticationError
import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from .routers import post, users, authentication

# from other file import statements
from .database import engine
from . import models

# Define the settings.
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


app.include_router(post.router)
app.include_router(users.router)
app.include_router(authentication.router)

@app.get("/")
def read_root():
    return {"Hello": "Partha_Sarathi_Chakraborty"}
 




  