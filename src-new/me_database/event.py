#!/usr/bin/env python3
""",
    me_database - event.py
    Author: Daryl Stark

    Event class for events
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Event(Database.base_class):
    """ Event class for events """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'events'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('unique'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    added =         Column(DateTime, nullable = False)
    changed =       Column(DateTime, nullable = False)
    tracked =       Column(Integer, default = 0, nullable = False)
    new =           Column(Boolean, default = False, nullable = False)
    title =         Column(String(256), nullable = False)
    support =       Column(String(256))
    stage =         Column(ForeignKey("stages.id"), nullable = True)
    date =          Column(Date)
    price =         Column(Integer)
    free =          Column(Boolean)
    soldout =       Column(Boolean)
    doorsopen =     Column(Time)
    starttime =     Column(Time)
    url =           Column(String(256), nullable = False)
    url_tickets =   Column(String(256))
    image =         Column(String(256))
    unique =        Column(String(256), nullable = False)
    cancelled =     Column(Boolean)
#---------------------------------------------------------------------------------------------------