#---------------------------------------------------------------------------------------------------
# EventSyncResult.py
#
# Date: 2019-01-10
#
# Class for sync results. A sync result is the result of a event synchronization
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class EventSyncResult(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tEventSyncResults'

    # Create the columns
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