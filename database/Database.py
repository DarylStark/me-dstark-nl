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
        self._echo = False

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
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError) as e:
            # When something goes wrong, do a rollback and return False so the caller can do a new
            # action. Note; if we don't do a rollback, the transaction will stay in place and the
            # next commit will fail too. So we always have to do a rollback!
            self._session.rollback()
            return False
#---------------------------------------------------------------------------------------------------