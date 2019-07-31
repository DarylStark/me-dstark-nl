#!/usr/bin/env python3
""",
    me_database - venue.py
    Author: Daryl Stark

    Venue class for venues
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Venue(Database.base_class):
    """ Venue class for venues """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tVenues'

    # Set constrains for this table
    __table_args__ = (
        sqlalchemy.UniqueConstraint('Venue_Name'),
    )

    # Database columns for this table
    id = sqlalchemy.Column('Venue_ID', sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column('Venue_Name', sqlalchemy.VARCHAR(128), nullable = False) 
#---------------------------------------------------------------------------------------------------