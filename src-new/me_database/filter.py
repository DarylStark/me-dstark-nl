#!/usr/bin/env python3
""",
    me_database - filter.py
    Author: Daryl Stark

    Table for filters
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class Filter(Database.base_class):
    """ Table for filters """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'filters'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('page', 'name'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    page =          Column(String(128), nullable = False)
    name =          Column(String(128), nullable = False)
    filter =        Column(String(512), nullable = False)
#---------------------------------------------------------------------------------------------------