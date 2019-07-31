#!/usr/bin/env python3
""",
    me_database - feeditemeventchange.py
    Author: Daryl Stark

    Table to connect Feeditems to Event Changes
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from me_database import Database
#---------------------------------------------------------------------------------------------------
class FeedItemEventChange(Database.base_class):
    """ Table to connect Feeditems to Event Changes """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'tFeedItemsEventChanges'

    # Database columns for this table
    id = sqlalchemy.Column('FeedItemChangeEvent_ID', sqlalchemy.Integer, primary_key = True)
    feeditem = sqlalchemy.Column('FeedItemChangeEvent_FeedItem', sqlalchemy.ForeignKey("tFeedItems.FeedItem_ID"), nullable = False)
    eventchange = sqlalchemy.Column('FeedItemChangeEvent_EventChange', sqlalchemy.ForeignKey("tEventChanges.EventChange_ID"), nullable = False)
#---------------------------------------------------------------------------------------------------