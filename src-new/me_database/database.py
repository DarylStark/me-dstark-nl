#!/usr/bin/env python3
"""
    me_database - database
    Author: Daryl Stark

    Main class for the Database object. Will be an static class that cannot be initiated.
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#---------------------------------------------------------------------------------------------------
class Database():
    """ Main class for the Database object. Will be an static class that cannot be initiated. """
    
    _engine = None
    base_class = declarative_base()
    session = sessionmaker()

    def __new__(cls, *args, **kwargs):
        """ The __new__ method is called before __init__ and is repsponsible for creating the new
            instance of the class. When a user tries to create a instance of this class, we raise an
            error """
        raise TypeError('It is not possible to create instances of Database')

    @classmethod
    def connect(cls, connection, echo = False, pool_pre_ping = True, pool_recycle = 10, pool_size = 5, pool_overflow = 10):
        """ Method to create a SQLAlchemy engine. Uses the database and credentials given by the
            user. Since this is a static class, we set it in the class parameter. This way, the
            complete application uses the same database engine. After creating the engine, it calls
            the command to create the tables in the database. 
            
            This method has a few parameters for creating the engine:
            - echo:          Can be used for debugging; writes the queries for SQLAlchemy to the
                             stdout buffer
            - pool_pre_ping: By default True. Determines if SQLAlchemy should do a pre-check before
                             using a connection that is already in the pool. By doing this, we can
                             prevent it from using dead connections
            - pool_recycle:  After how many seconds SQLAlchemy considers a MySQL connection to be
                             stale and therefore removed from the database
            - pool_size:     The size the pool can get
            - pool_overflow: How many connections SQLAlchemy can go over the pool_size
        """
        
        # Create the engine
        cls._engine = create_engine(
            connection,
            echo = echo,
            pool_pre_ping = pool_pre_ping,
            pool_recycle = pool_recycle,
            pool_size = pool_size,
            max_overflow = pool_overflow
        )

        # Create the configured tables
        cls.base_class.metadata.create_all(cls._engine)

        # Bind the engine to the sessionmaker of the class
        cls.session.configure(bind = cls._engine)
#---------------------------------------------------------------------------------------------------
