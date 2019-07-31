#!/usr/bin/env python3
""",
    me_database - venue.py
    Author: Daryl Stark

    Venue class for venues
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Venue(Database.base_class):
    """ Venue class for venues """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'venues'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('name'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    name =          Column(String(128), nullable = False)

    # One-to-many relationship mappings
    stages = relationship("Stage")
#---------------------------------------------------------------------------------------------------