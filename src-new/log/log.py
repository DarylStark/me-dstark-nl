#!/usr/bin/env python3
"""
    log - log.py

    Contains the main class for the Logger; writes logging to whever it needs to go
"""
#---------------------------------------------------------------------------------------------------
# Imports
import datetime
import sys
import sqlalchemy
import os
#---------------------------------------------------------------------------------------------------
# The names for the emergency levels
severity_names = [
    'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'
]
#---------------------------------------------------------------------------------------------------
class Log:
    """ Class to log information to whever it needs to go """

    # TODO: Add to unittests

    # Constans for output streams
    STREAM_STDOUT = 1
    STREAM_STDERR = 2
    STREAM_DATABASE = 3

    # Constants for severity levels
    DEBUG = 7
    INFO = 6
    NOTICE = 5
    WARNING = 4
    ERROR = 3
    CRITICAL = 2
    ALERT = 1
    EMERGENCY = 0

    # Set with the default streams to output to
    _default_output_streams = {
        STREAM_STDOUT
    }

    # The format_console class variable defines how to display messages on the console
    format_console = '[ {date} | {time} ] [ {severity: <9} ] [ {pid: 5d} ] [ {module: <16} ] {message}'

    # Objects for database interconnection
    database_object = None
    database_entry_object = None

    # The verbosity_level_console defines what the maximum level of messages is that will be
    # displayed. Each level above this isn't displayed. It defaults to six (info-messages), but this
    # can be changed by the user
    verbosity_level_console = INFO

    # Database entry backlog. We fill this when the user wants to write to the database
    _database_backlog = list()

    # Variable that holds the PID for the process. This is set the first time the 'log' method is
    # called and will be used for each log message. This makes sure the logging can be put together
    # for specific threads
    _pid = None

    def __new__(cls, *args, **kwargs):
        """ The __new__ method is called before __init__ and is repsponsible for creating the new
            instance of the class. When a user tries to create a instance of this class, we raise an
            error """
        raise TypeError('It is not possible to create instances of CheckFactory')
    
    @classmethod
    def log(cls, message, severity = INFO, streams = None, module = '', **kwargs):
        """ Method to log something """

        # Get the current date and time for later
        now = datetime.datetime.now()

        # Check if we have a PID in the local class. If we don't, set it
        if cls._pid is None:
            cls._pid = os.getpid()

        # Find out what streams we need to write to
        if streams == None:
            streams = cls._default_output_streams

        # Check if we need to write to STDOUT or STDERR
        for stream in (cls.STREAM_STDERR, cls.STREAM_STDOUT):
            if stream in streams:
                # Get the correct output stream
                if stream == cls.STREAM_STDERR: outstream = sys.stderr
                if stream == cls.STREAM_STDOUT: outstream = sys.stdout
                
                # Write to the correct place
                if severity <= cls.verbosity_level_console:
                    print(
                        cls.format_console.format(
                            date = now.strftime('%Y.%m.%d'),
                            time = now.strftime('%H:%M:%S.%f')[:-3],
                            severity = severity_names[severity],
                            message = str(message),
                            module = module,
                            pid = cls._pid,
                            **kwargs
                        ),
                        end = '\n',
                        file = outstream
                    )
        
        # Check if we need to write to the database
        if cls.STREAM_DATABASE in streams:
            # If we need to write the logentry to the database, we create an object for this and add
            # this object to a stack. This stack gets later written to database, if there is a
            # database connection available. If there isn't, then entries stay in the stack. This
            # way, we can buffer writing to database for when the application is getting initialized
            # and the database is not ready yet.
            
            # Check if the objects are configured
            if not cls.database_object is None and not cls.database_entry_object is None:
                # MySQL writes out the time rounded up using the microseconds. This results in weird
                # times, so we remove the microseconds. We also store the microseconds though, so we
                # have to save them prior to removing them
                microseconds = round(now.microsecond / 1000)
                now = now.replace(microsecond = 0)

                # Create a object for the log entry
                entry = cls.database_entry_object(
                    datetime = now,
                    microsecond = microseconds,
                    severity = severity,
                    pid = cls._pid,
                    module = module,
                    message = str(message),
                    **kwargs
                )

                # Add the entry to the backlog
                cls._database_backlog.append(entry)

                # Write out the backlog
                cls.process_backlog()
    
    @classmethod
    def process_backlog(cls):
        """ Method that actually processes the database backlog. Only processes the backlog when the
            _engine method in the Database-object is not None, meaning the database is ready """
        
        if not cls.database_object is None:
            if not cls.database_object._engine is None:
                # Create a database session, add the entries and commit it
                session = cls.database_object.session()
                session.add_all(cls._database_backlog)

                # We are going to write the entries in the backlog to the database. If we receive a
                # UnboundExecutionError, the database wasn't ready yet to write data
                try:
                    # Commit it
                    session.commit()
                except sqlalchemy.exc.UnboundExecutionError:
                    # Close the session. We will try again later
                    session.close()
                else:
                    # Empty the backlog
                    cls._database_backlog = list()
    
    @classmethod
    def add_default_stream(cls, stream):
        """ Method to add a default stream to the class """
        cls._default_output_streams.add(stream)
#---------------------------------------------------------------------------------------------------