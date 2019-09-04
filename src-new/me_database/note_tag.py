#!/usr/bin/env python3
""",
    me_database - note_tag.py
    Author: Daryl Stark

    Table for tags for notes
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class NoteTag(Database.base_class):
    """ Table for tags for notes """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'note_tags'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('name', 'parent'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    name =          Column(String(128), nullable = False)
    parent =        Column(ForeignKey("note_tags.id"), nullable = True)
#---------------------------------------------------------------------------------------------------