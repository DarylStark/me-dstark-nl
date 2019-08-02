#!/usr/bin/env python3
"""
    me_database - feed_item
    Author: Daryl Stark

    Table for feed items
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class FeedItem(Database.base_class):
    """ Table for feed items """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'feed_items'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    date =          Column(DateTime, nullable = False)
    changedate =    Column(DateTime, nullable = False)
    itemtype =      Column(Integer, nullable = False)
    status =        Column(Integer, default = 1, nullable = False)
    event =         Column(ForeignKey("events.id"), nullable = True)

    # One-to-many relationship mappings
    feed_items_event_change = relationship("FeedItemEventChange")
#---------------------------------------------------------------------------------------------------