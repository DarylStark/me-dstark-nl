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

        # Create a session
        self._session_factory = sqlalchemy.orm.sessionmaker(bind = self._engine)
        self._session = self._session_factory()

        # Create the schema.
        database.BaseClass.metadata.create_all(self._engine)
    
    def commit(self):
        """ Commits the changes to the database """
        self._session.commit()
    
    #-----------------------------------------------------------------------------------------------
    # Methods for venues
    #-----------------------------------------------------------------------------------------------

    def venues(self):
        """ Returns the venues in the database """

        # Get the venues from the database
        venues = self._session.query(database.Venue)

        # Return the result
        return venues

    #-----------------------------------------------------------------------------------------------
    # Methods for events
    #-----------------------------------------------------------------------------------------------

    def add_event(self, event):
        """ Adds a event to the database """

        # Set the Event_Added and Event_Changed to the current date
        event.added = datetime.datetime.utcnow()
        event.changed = datetime.datetime.utcnow()

        try:
            # Add the event and commit the changes
            self._session.add(event)
            self._session.commit()

            # Everything went fine, return True
            return True
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
            # When something goes wrong, do a rollback and return False so the caller can do a new
            # action. Note; if we don't do a rollback, the transaction will stay in place and the
            # next commit will fail too. So we always have to do a rollback!
            self._session.rollback()
            return False

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
            return attribute
        
        # They were the same, return None
        return None
    
    def sync_event(self, event):
        """ Checks if a event is already in the database. If it is, it updates it. If it isn't, it
            adds the event using the add_event method of this class. Returns True when the object
            was added. Returns False when something went wrong. Returns a list with changed
            properties when the object already existed. """
        
        # First, try to add the event. If it succeeds, we are done. If it doesn't succeed, the
        # object is already in the database and we can search for the original one
        if self.add_event(event) == False:
            try:
                # Find the original event
                original_events = self._session.query(database.Event).filter(
                    database.Event.unique == event.unique
                )

                # Get the original event
                original_event = original_events[0]

                # Update the original event and keep track of the made changes
                attributes = [
                    'title', 'support', 'venue', 'stage',
                    'date', 'price', 'free', 'soldout',
                    'doorsopen', 'starttime', 'url', 'url_tickets',
                    'image'
                ]
                changes = [ self.compare_and_set_attribute(attribute, original_event, event) for attribute in attributes ]

                # Remove all None's from the list
                changes = [ change for change in changes if change is not None ]

                # If the object has changed, update the 'change' field of the object
                if len(changes) > 0:
                    original_event.changed = datetime.datetime.utcnow()

                # Commit the new changes
                self._session.commit()

                # TODO: create a log entry for this event

                # Return the created list with changes
                return changes
            except KeyboardInterrupt:
                # Something went wrong, return False
                return False

        # We return a tuple with only True when the code above isn't execute
        return True
#---------------------------------------------------------------------------------------------------