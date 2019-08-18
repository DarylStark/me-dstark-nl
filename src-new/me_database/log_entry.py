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
from sqlalchemy.dialects import mysql
#---------------------------------------------------------------------------------------------------
class LogEntry(Database.base_class):
    """ Database object for log entries """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'log'

    # We create a separate column for microseconds since MySQL doesn't store microseconds in the
    # DateTime datatype. The calling function have to add this field.

    # Database columns for this table
    id =            Column(Integer, primary_key = True, nullable = False)
    datetime =      Column(DateTime, nullable = False)
    microsecond =   Column(mysql.SMALLINT, nullable = False)
    severity =      Column(Integer, nullable = False)
    pid =           Column(Integer, nullable = False)
    module =        Column(String(128), nullable = False)
    message =       Column(String(1024), nullable = False)
    
    # Application specific fields for the log
    sync_result =   Column(ForeignKey("event_sync_results.id"), nullable = True)
#---------------------------------------------------------------------------------------------------
