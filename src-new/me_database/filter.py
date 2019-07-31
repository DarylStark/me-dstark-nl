#!/usr/bin/env python3
""",
    me_database - filter.py
    Author: Daryl Stark

    Column for filters
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Filter(Database.base_class):
    """ Column for filters """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tFilters'

    # Database columns for this table
    id = sqlalchemy.Column('Filter_ID', sqlalchemy.Integer, primary_key = True)
    page = sqlalchemy.Column('Filter_Page', sqlalchemy.Text, nullable = False)
    name = sqlalchemy.Column('Filter_Name', sqlalchemy.Text, nullable = False)
    filter = sqlalchemy.Column('Filter_Filter', sqlalchemy.Text, nullable = False)
#---------------------------------------------------------------------------------------------------