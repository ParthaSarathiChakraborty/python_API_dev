from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Partha_Sarathi_Chakraborty"}

@app.get("/post")
def user_post():
    return {"Post": "This is your Partha Sarathi 01"}

