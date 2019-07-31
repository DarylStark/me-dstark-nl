#!/usr/bin/env python3
""",
    me_database - feeditemeventchange.py
    Author: Daryl Stark

    Table to connect feed items to event changes
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class FeedItemEventChange(Database.base_class):
    """ Table to connect feed items to event changes """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'feed_item_event_changes'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    feeditem =      Column(ForeignKey("feed_items.id"), nullable = False)
    eventchange =   Column(ForeignKey("event_changes.id"), nullable = False)
#---------------------------------------------------------------------------------------------------