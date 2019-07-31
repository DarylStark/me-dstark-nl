#!/usr/bin/env python3
""",
    me_database - event.py
    Author: Daryl Stark

    Event class for events
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Event(Database.base_class):
    """ Event class for events """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tEvents'

    # Database columns for this table
    id = sqlalchemy.Column('Event_ID', sqlalchemy.Integer, primary_key = True)
    added = sqlalchemy.Column('Event_Added', sqlalchemy.DateTime, nullable = False)
    changed = sqlalchemy.Column('Event_Changed', sqlalchemy.DateTime, nullable = False)
    tracked = sqlalchemy.Column('Event_Tracked', sqlalchemy.Integer, default = 0, nullable = False)
    new = sqlalchemy.Column('Event_New', sqlalchemy.Boolean, default = False, nullable = False)
    title = sqlalchemy.Column('Event_Title', sqlalchemy.Text, nullable = False)
    support = sqlalchemy.Column('Event_Support', sqlalchemy.Text)
    stage = sqlalchemy.Column('Event_Stage', sqlalchemy.ForeignKey("tStages.Stage_ID"), nullable = True)
    date = sqlalchemy.Column('Event_Date', sqlalchemy.Date)
    price = sqlalchemy.Column('Event_Price', sqlalchemy.Integer)
    free = sqlalchemy.Column('Event_Free', sqlalchemy.Boolean)
    soldout = sqlalchemy.Column('Event_Soldout', sqlalchemy.Boolean)
    doorsopen = sqlalchemy.Column('Event_DoorsOpen', sqlalchemy.Time)
    starttime = sqlalchemy.Column('Event_StartTime', sqlalchemy.Time)
    url = sqlalchemy.Column('Event_URL', sqlalchemy.Text, nullable = False)
    url_tickets = sqlalchemy.Column('Event_URLTickets', sqlalchemy.Text)
    image = sqlalchemy.Column('Event_Image', sqlalchemy.Text)
    unique = sqlalchemy.Column('Event_Unique', sqlalchemy.VARCHAR(length = 128), nullable = False)
#---------------------------------------------------------------------------------------------------