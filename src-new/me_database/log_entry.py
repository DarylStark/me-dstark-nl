#!/usr/bin/env python3
"""
    me_database - log_entry
    Author: Daryl Stark

    Database object for log entries
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from me_database import Database
#---------------------------------------------------------------------------------------------------
class LogEntry(Database.base_class):
    """ Database object for log entries """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'log'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    datetime =      Column(DateTime())
    severity =      Column(Integer)
    module =        Column(String(128))
    message =       Column(String(1024))
#---------------------------------------------------------------------------------------------------
