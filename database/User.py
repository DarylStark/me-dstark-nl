#---------------------------------------------------------------------------------------------------
# User.py
#
# Date: 2019-01-09
#
# Class for users. A user is someone who is allowed to log in.
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class User(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tUsers'

    # Set constrains for this table
    __table_args__ = (
        sqlalchemy.UniqueConstraint('User_EMail'),
    )

    # Create the columns
    id = sqlalchemy.Column('User_ID', sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column('User_Name', sqlalchemy.VARCHAR(128), nullable = True)
    email = sqlalchemy.Column('User_EMail', sqlalchemy.VARCHAR(128), nullable = False)
    googleid = sqlalchemy.Column('User_GoogleID', sqlalchemy.VARCHAR(128), nullable = True)
    image = sqlalchemy.Column('User_Image', sqlalchemy.VARCHAR(128), nullable = True)
#---------------------------------------------------------------------------------------------------