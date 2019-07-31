#!/usr/bin/env python3
""",
    me_database - stage.py
    Author: Daryl Stark

    Class for stages
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Stage(Database.base_class):
    """ Class for stages """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tStages'

    # Database columns for this table
    id = sqlalchemy.Column('Stage_ID', sqlalchemy.Integer, primary_key = True)
    venue = sqlalchemy.Column('Stage_Venue', sqlalchemy.ForeignKey("tVenues.Venue_ID"), nullable = False)
    name = sqlalchemy.Column('Stage_Name', sqlalchemy.VARCHAR(128))
    address = sqlalchemy.Column('Stage_Address', sqlalchemy.Text)
    zipcode = sqlalchemy.Column('Stage_Zipcode', sqlalchemy.Text)
    city = sqlalchemy.Column('Stage_City', sqlalchemy.Text)
    country = sqlalchemy.Column('Stage_Country', sqlalchemy.Text)
#---------------------------------------------------------------------------------------------------