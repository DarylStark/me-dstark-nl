#!/usr/bin/env python3
""",
    me_database - event_change.py
    Author: Daryl Stark

    Class for Event Change history
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class EventChange(Database.base_class):
    """ Class for Event Change history """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'event_changes'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    event =         Column(ForeignKey("events.id"), nullable = False)
    changed =       Column(DateTime, nullable = False)
    field =         Column(String(256))
    oldvalue =      Column(String(256))
    newvalue =      Column(String(256))
#---------------------------------------------------------------------------------------------------