#---------------------------------------------------------------------------------------------------
# Database.py
#
# Date: 2018-12-21
#
# Class for a Database connection. Retrieves information from the database
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
import os
import datetime
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class Database:
    """ Class to open database connections and retrieve information from the database """

    def __init__(self):
        """ Sets default variables """

        # Create an empty dict for the table-objects
        self._tables = {}

        # None-object for metadata
        self._metadata = None

        # Set the Development credentials
        self._host = os.getenv('DEV_SQL_SERVER', '')
        self._username = os.getenv('DEV_SQL_USERNAME', '')
        self._password = os.getenv('DEV_SQL_PASSWORD', '')
        self._database = os.getenv('DEV_SQL_DATABASE', '')
        self._connection = None
        self._echo = True

        # Check if we are on the production environment and set the values for production
        if 'gunicorn' in os.getenv('SERVER_SOFTWARE', ''):
            self._host = os.getenv('PROD_SQL_SERVER', '')
            self._username = os.getenv('PROD_SQL_USERNAME', '')
            self._password = os.getenv('PROD_SQL_PASSWORD', '')
            self._database = os.getenv('PROD_SQL_DATABASE', '')
            self._connection = None
            self._echo = False

        # Create the connection string that is needed when we create a connection
        # TODO: create a connection string for Google SQL
        self.connection_string = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
            username = self._username,
            password = self._password,
            host = self._host,
            database = self._database
        )

        # Create a SQLalchemy engine that we can use later on
        self._engine = sqlalchemy.create_engine(
            self.connection_string,
            echo = self._echo
        )

        # Create a session-factory
        self._session_factory = sqlalchemy.orm.sessionmaker(bind = self._engine)

        # Create the schema.
        database.BaseClass.metadata.create_all(self._engine)
    
    def compare_and_set_attribute(self, attribute, object_a, object_b):
        """ Compares a attribute in two objects. If they are different, it sets the var in object
            A to the same value as in object B and returns the name of the object. If they are the
            same, it doesn't update anything and returns None """

        # Get the values
        var_a = getattr(object_a, attribute)
        var_b = getattr(object_b, attribute)

        # Compare the values
        if var_a != var_b:
            # Not the same, so we have to set the value in A to the same as in B
            setattr(object_a, attribute, var_b)

            # And return the name of the attribute
            return attribute, var_a, var_b
        
        # They were the same, return None
        return None
    
    #-----------------------------------------------------------------------------------------------
    # Methods for venues
    #-----------------------------------------------------------------------------------------------

    def venues(self):
        """ Returns the venues in the database """

        # Get the venues from the database
        session = self._session_factory()
        venues = session.query(database.Venue)

        # Return the result
        return venues
    
    #-----------------------------------------------------------------------------------------------
    # Methods for stages
    #-----------------------------------------------------------------------------------------------

    def stages(self, venue = None):
        """ Returns the stages from the database, filtered on venue if needed """

        # Get the stages from the database
        session = self._session_factory()
        stages = session.query(database.Stage).filter(
            database.Stage.venue == venue
        )

        # Return the result
        return stages

    #-----------------------------------------------------------------------------------------------
    # Methods for events
    #-----------------------------------------------------------------------------------------------

    def events(self, unique = None):
        """ Returns the events from the database, filtered if needed """

        # Get the stages from the database
        session = self._session_factory()
        events = session.query(database.Event).filter(
            database.Event.unique == unique
        )

        # Return the result
        return events
 
    #-----------------------------------------------------------------------------------------------
    # Methods for feed items
    #-----------------------------------------------------------------------------------------------
    
    def feeditems(self):
        """ Returns the feeditems from the database, filtered if needed """

        # Get the feeditems from the database. We do a 'outer' join with the Event table to
        # retrieve all events that are related to the feeditems. This results in a LEFT OUTER
        # join.
        session = self._session_factory()
        feeditems = session.query(database.FeedItem).add_entity(database.Event).outerjoin(database.Event)

        # Return the result
        return feeditems
    
    #-----------------------------------------------------------------------------------------------
    # Methods for feed items / change events
    #-----------------------------------------------------------------------------------------------
  
    def feed_item_event_changes(self, feeditem = None):
        """ Returns the feeditemeventchanges from the database, filtered if needed """

        # Get the feeditemseventchanges from the database, filtered on the requested feeditem
        session = self._session_factory()
        changes = session.query(database.FeedItemEventChange).add_entity(database.EventChange).outerjoin(database.EventChange)

        # Return the result
        return changes
#---------------------------------------------------------------------------------------------------