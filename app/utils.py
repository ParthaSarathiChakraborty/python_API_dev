# This file will contain a bunch of utility functions.

from passlib.context import CryptContext

# Define the settings.
# This is the hashing algorithm: bcrypt.
pwd_context = CryptContext (schemes=["bcrypt"], deprecated="auto")

# Hash function to hash the passwords.
def hash_function(password: str):
    return pwd_context.hash(password)


# Password check logic.

def verify(plain_pass, hashed_pass):
     return pwd_context.verify(plain_pass, hashed_pass ) 