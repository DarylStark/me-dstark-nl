#!/usr/bin/env python3
""",
    me_database - user.py
    Author: Daryl Stark

    User column for users who are allowed to log in
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class User(Database.base_class):
    """ User column for users who are allowed to log in """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'users'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    name =          Column(String(128), nullable = True)
    email =         Column(String(128), nullable = False)
    googleid =      Column(String(128), nullable = True)
    image =         Column(String(128), nullable = True)
#---------------------------------------------------------------------------------------------------