#---------------------------------------------------------------------------------------------------
# Event.py
#
# Date: 2018-12-22
#
# Class for events. A event holds all data that is needed for events. 
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class Event(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tEvents'

    # Set constrains for this table
    __table_args__ = (
        sqlalchemy.UniqueConstraint('Event_Unique'),
    )

    # Create the columns
    id = sqlalchemy.Column('Event_ID', sqlalchemy.Integer, primary_key = True)
    added = sqlalchemy.Column('Event_Added', sqlalchemy.DateTime, nullable = False)
    changed = sqlalchemy.Column('Event_Changed', sqlalchemy.DateTime, nullable = False)
    tracked = sqlalchemy.Column('Event_Tracked', sqlalchemy.Boolean, default = False, nullable = False)
    new = sqlalchemy.Column('Event_New', sqlalchemy.Boolean, default = False, nullable = False)
    title = sqlalchemy.Column('Event_Title', sqlalchemy.Text, nullable = False)
    support = sqlalchemy.Column('Event_Support', sqlalchemy.Text)
    venue = sqlalchemy.Column('Event_Venue', sqlalchemy.Text, nullable = False)
    stage = sqlalchemy.Column('Event_Stage', sqlalchemy.Text, nullable = False)
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