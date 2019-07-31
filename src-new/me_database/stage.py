#!/usr/bin/env python3
""",
    me_database - stage.py
    Author: Daryl Stark

    Table for stages
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Stage(Database.base_class):
    """ Table for stages """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'stages'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('venue', 'name'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    venue =         Column(ForeignKey("venues.id"), nullable = False)
    name =          Column(String(128))
    address =       Column(String(128))
    zipcode =       Column(String(128))
    city =          Column(String(128))
    country =       Column(String(128))

    # One-to-many relationship mappings
    events = relationship("Event")
#---------------------------------------------------------------------------------------------------