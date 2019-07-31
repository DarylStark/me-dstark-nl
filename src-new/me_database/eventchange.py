#!/usr/bin/env python3
""",
    me_database - eventchange.py
    Author: Daryl Stark

    Class for Event Change history
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class EventChange(Database.base_class):
    """ Class for Event Change history """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tEventChanges'

    # Database columns for this table
    id = sqlalchemy.Column('EventChange_ID', sqlalchemy.Integer, primary_key = True)
    event = sqlalchemy.Column('EventChange_Event', sqlalchemy.ForeignKey("tEvents.Event_ID"), nullable = False)
    changed = sqlalchemy.Column('EventChange_Changed', sqlalchemy.DateTime, nullable = False)
    field = sqlalchemy.Column('EventChange_Field', sqlalchemy.Text)
    oldvalue = sqlalchemy.Column('EventChange_Old_Value', sqlalchemy.Text)
    newvalue = sqlalchemy.Column('EventChange_New_Value', sqlalchemy.Text)
#---------------------------------------------------------------------------------------------------