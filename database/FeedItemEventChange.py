#---------------------------------------------------------------------------------------------------
# FeedItemEventChange.py
#
# Date: 2018-12-27
#
# Class to connect feed items to changed events
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class FeedItemEventChange(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tFeedItemsEventChanges'

    # Create the columns
    id = sqlalchemy.Column('FeedItemChangeEvent_ID', sqlalchemy.Integer, primary_key = True)
    feeditem = sqlalchemy.Column('FeedItemChangeEvent_FeedItem', sqlalchemy.ForeignKey("tFeedItems.FeedItem_ID"), nullable = False)
    eventchange = sqlalchemy.Column('FeedItemChangeEvent_EventChange', sqlalchemy.ForeignKey("tEventChanges.EventChange_ID"), nullable = False)
#---------------------------------------------------------------------------------------------------