#!/usr/bin/env python3
""",
    me_database - note.py
    Author: Daryl Stark

    Table for notes
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class Note(Database.base_class):
    """ Table for notes """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'notes'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    created =       Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    title =         Column(String(256), nullable = False)

    # Many-to-one relationship mappings
    revisions = relationship("NoteRevision")
#---------------------------------------------------------------------------------------------------