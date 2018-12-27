#---------------------------------------------------------------------------------------------------
# EventChange.py
#
# Date: 2018-12-27
#
# Class for events changes. A event change holds a change for a event
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class EventChange(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tEventChanges'

    # Create the columns
    id = sqlalchemy.Column('EventChange_ID', sqlalchemy.Integer, primary_key = True)
    event = sqlalchemy.Column('EventChange_Event', sqlalchemy.ForeignKey("tEvents.Event_ID"), nullable = False)
    changed = sqlalchemy.Column('EventChange_Changed', sqlalchemy.DateTime, nullable = False)
    field = sqlalchemy.Column('EventChange_Field', sqlalchemy.Text)
    oldvalue = sqlalchemy.Column('EventChange_Old_Value', sqlalchemy.Text)
    newvalue = sqlalchemy.Column('EventChange_New_Value', sqlalchemy.Text)
#---------------------------------------------------------------------------------------------------