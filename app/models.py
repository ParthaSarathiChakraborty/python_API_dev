# Models represents a table in a database.

# from database import Base:
# This import statement imports the Base object directly from the database module. It assumes that the database module is accessible from the current module or from the PYTHONPATH. This form of import is typically used when the module being imported is in the same directory or available in the global namespace.

# from .database import Base:
# The . preceding the module name indicates a relative import. This import statement imports the Base object from the database module relative to the current module's package. The . refers to the current package or module's location. This form of import is commonly used when importing from modules within the same package or subpackages.

########### ########### ########### ########### ########### ###########
# This file creates a table with a defined schema in the Postgres database.
########### ########### ########### ########### ########### ###########

from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

# Creates a table 'post' if not exists with the schema defined below.
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    # Define the foreign key relationship with the User model
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship("User")




# Creates a table named 'users', which will contain the user information after they have registered.
    
class User(Base):
    __tablename__ = 'users'
    
    # Schema/Column in the database.   
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=text('now()'))
    