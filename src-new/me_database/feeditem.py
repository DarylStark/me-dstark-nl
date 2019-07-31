#!/usr/bin/env python3
"""
    me_database - test
    Author: Daryl Stark

    Database object for feed items
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from me_database import Database
#---------------------------------------------------------------------------------------------------
class FeedItem(Database.base_class):
    """ Database object for checks feed items """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tFeedItems'

    # Database columns for this table
    id = sqlalchemy.Column('FeedItem_ID', sqlalchemy.Integer, primary_key = True)
    date = sqlalchemy.Column('FeedItem_Date', sqlalchemy.DateTime, nullable = False)
    changedate = sqlalchemy.Column('FeedItem_ChangeDate', sqlalchemy.DateTime, nullable = False)
    itemtype = sqlalchemy.Column('FeedItem_Type', sqlalchemy.Integer, nullable = False)
    status = sqlalchemy.Column('FeedItem_Status', sqlalchemy.Integer, default = 1, nullable = False)
    event = sqlalchemy.Column('FeedItem_Event', sqlalchemy.ForeignKey("tEvents.Event_ID"))
#---------------------------------------------------------------------------------------------------