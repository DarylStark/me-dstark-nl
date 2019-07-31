#!/usr/bin/env python3
""",
    me_database - user.py
    Author: Daryl Stark

    User column for users who are allowed to log in
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class User(Database.base_class):
    """ User column for users who are allowed to log in """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tUsers'

    # Database columns for this table
    id = sqlalchemy.Column('User_ID', sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column('User_Name', sqlalchemy.VARCHAR(128), nullable = True)
    email = sqlalchemy.Column('User_EMail', sqlalchemy.VARCHAR(128), nullable = False)
    googleid = sqlalchemy.Column('User_GoogleID', sqlalchemy.VARCHAR(128), nullable = True)
    image = sqlalchemy.Column('User_Image', sqlalchemy.VARCHAR(128), nullable = True)
#---------------------------------------------------------------------------------------------------