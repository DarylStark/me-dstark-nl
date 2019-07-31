#!/usr/bin/env python3
""",
    me_database - event_sync_result.py
    Author: Daryl Stark

    Table to log synchronization results for events
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class EventSyncResult(Database.base_class):
    """ Table to log synchronization results for events """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'event_sync_results'

    # Database columns for this table
    id =                Column(Integer, primary_key = True)
    datetime =          Column(DateTime, nullable = False)
    runtime =           Column(Integer, nullable = False)
    service =           Column(String(256), nullable = False)
    cron =              Column(Boolean, nullable = False)
    success =           Column(Boolean, nullable = False)
    found =             Column(Integer)
    errors =            Column(Integer)
    new_events =        Column(Integer)
    updated_events =    Column(Integer)
#---------------------------------------------------------------------------------------------------