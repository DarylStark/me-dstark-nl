#!/usr/bin/env python3
""",
    me_database - user_session.py
    Author: Daryl Stark

    Table for user sessions
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class UserSession(Database.base_class):
    """ Table for user sessions """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'user_sessions'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('secret'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    start =         Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    user =          Column(ForeignKey("users.id"), nullable = False)
    ipv4_address =  Column(String(16), nullable = True)
    ipv6_address =  Column(String(40), nullable = True)
    secret =        Column(String(32), nullable = False)
#---------------------------------------------------------------------------------------------------