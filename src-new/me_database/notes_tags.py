#!/usr/bin/env python3
""",
    me_database - notes_tags.py
    Author: Daryl Stark

    Table to connect notes to tags
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class NotesTags(Database.base_class):
    """ Table to connect notes to tags """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'notes_tags'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('tag', 'note'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    tag =           Column(ForeignKey("note_tags.id"), nullable = False)
    note =          Column(ForeignKey("notes.id"), nullable = False)

    # Connected objects
    tag_object = relationship("NoteTag")
    note_object = relationship("Note")
#---------------------------------------------------------------------------------------------------