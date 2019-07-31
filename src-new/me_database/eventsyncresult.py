#!/usr/bin/env python3
""",
    me_database - eventsyncresult.py
    Author: Daryl Stark

    Table to log Synchronization results for events
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class EventSyncResult(Database.base_class):
    """ Table to log Synchronization results for events """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tEventSyncResults'

    # Database columns for this table
    id = sqlalchemy.Column('Result_ID', sqlalchemy.Integer, primary_key = True)
    datetime = sqlalchemy.Column('Result_DateTime', sqlalchemy.DateTime, nullable = False)
    runtime = sqlalchemy.Column('Result_Runtime', sqlalchemy.Integer, nullable = False)
    service = sqlalchemy.Column('Result_Service', sqlalchemy.VARCHAR(128), nullable = False)
    cron = sqlalchemy.Column('Result_Cron', sqlalchemy.Boolean, nullable = False)
    success = sqlalchemy.Column('Result_Success', sqlalchemy.Boolean, nullable = False)
    found = sqlalchemy.Column('Result_Found', sqlalchemy.Integer)
    errors = sqlalchemy.Column('Result_Errors', sqlalchemy.Integer)
    new_events = sqlalchemy.Column('Result_New', sqlalchemy.Integer)
    updated_events = sqlalchemy.Column('Result_Updated', sqlalchemy.Integer)
#---------------------------------------------------------------------------------------------------