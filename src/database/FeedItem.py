#---------------------------------------------------------------------------------------------------
# FeedItem.py
#
# Date: 2018-12-27
#
# Class for feed items
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class FeedItem(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tFeedItems'

    # Create the columns
    id = sqlalchemy.Column('FeedItem_ID', sqlalchemy.Integer, primary_key = True)
    date = sqlalchemy.Column('FeedItem_Date', sqlalchemy.DateTime, nullable = False)
    changedate = sqlalchemy.Column('FeedItem_ChangeDate', sqlalchemy.DateTime, nullable = False)
    itemtype = sqlalchemy.Column('FeedItem_Type', sqlalchemy.Integer, nullable = False)
    status = sqlalchemy.Column('FeedItem_Status', sqlalchemy.Integer, default = 1, nullable = False)
    event = sqlalchemy.Column('FeedItem_Event', sqlalchemy.ForeignKey("tEvents.Event_ID"))

    # Constants for event status
    STATUS_NEW = 1
    STATUS_SNOOZED = 2

    # Constants for event types
    TYPE_NEW_EVENT = 1
    TYPE_TRACKED_EVENT_CHANGED = 2
    TYPE_EVENT_CHANGED = 3

    def get_dict(self):
        """ Method to represent the object as a dict """

        return {
            'id': self.id,
            'date': self.date,
            'changedate': self.changedate,
            'itemtype': self.itemtype,
            'status': self.status,
            'event': self.event
        }
#---------------------------------------------------------------------------------------------------