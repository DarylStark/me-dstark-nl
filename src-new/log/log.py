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
import threading
#---------------------------------------------------------------------------------------------------
# The names for the emergency levels
severity_names = [
    'emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug'
]
#---------------------------------------------------------------------------------------------------
class Log:
    """ Class to log information to whever it needs to go """

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
    _database_backlog = set()
    _backlog_lock = threading.Lock()

    # How many items do have to be in the backlog before writing them out
    database_backlog_maxitems = 1

    # Extra fields for the logging. The fields configured here will have two properties; the name
    # and the value. The value can be an integer or string to present a static value, or it can be a
    # callable. In case of a callable, the result of the call will be used for the value. If it is a
    # callable, everytime a new log entry is created, the method gets called again. This way, the
    # user of the Log class can determine what gets filled in. It can be, for instance, a method
    # that returns the IP address in a Flask request.
    extra_fields = dict()

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

        # Get the PID for the current process
        pid = os.getpid()

        # If we have extra fields defined in the class, let's walk through them and add the elements
        # to the 'kwargs' variable. This variable will be used later with the representation of the
        # log items and when writing to the database.
        for field, value in cls.extra_fields.items():
            # Check if the value is a static value, or if it is callable. Set the 'newvalue'
            # variable to the correct newvalue which we will use later.
            newvalue = value
            if hasattr(value, '__call__'):
                newvalue = value()
            
            # Add it to 'kwargs'
            kwargs.update({ field: newvalue })

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
                            pid = pid,
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
                    pid = pid,
                    module = module,
                    message = str(message),
                    **kwargs
                )

                # Add the entry to the backlog
                cls._database_backlog.add(entry)

                # Write out the backlog
                cls.process_backlog()
    
    @classmethod
    def process_backlog(cls, force = False):
        """ Method that actually processes the database backlog. Only processes the backlog when the
            _engine method in the Database-object is not None, meaning the database is ready. We
            don't sync the database when there are less then cls.database_backlog_maxitems in the
            backlog. This way, we can spare database resources. We always write it out when the user
            specifies 'force'. """

        if len(cls._database_backlog) >= cls.database_backlog_maxitems or force:
            if not cls.database_object is None:
                if not cls.database_object._engine is None:
                    # Set a lock, so a seperate thread cannot write untill this is done
                    cls._backlog_lock.acquire()

                    # Create a session
                    session = cls.database_object.session()
                    
                    # Add all items to the session
                    session.add_all(cls._database_backlog)

                    # We are going to write the entries in the backlog to the database. If we receive a
                    # UnboundExecutionError, the database wasn't ready yet to write data
                    try:
                        # Commit it
                        session.commit()
                    except sqlalchemy.exc.UnboundExecutionError:
                        # If we get an unbound error, we just skip this backlog processing. We will
                        # get it next time
                        session.rollback()
                    
                    # Remove everything from the backlog
                    cls._database_backlog = set()

                    # Release the lock so seperate threads can do anything they want
                    cls._backlog_lock.release()

    @classmethod
    def add_default_stream(cls, stream):
        """ Method to add a default stream to the class """
        cls._default_output_streams.add(stream)
#---------------------------------------------------------------------------------------------------