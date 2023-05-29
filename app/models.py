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

# Creates a table 'post' if not exists with the schema defined below.
class Post(Base):
    __tablename__ = 'post'
    
    # This is the defined schema.
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    
