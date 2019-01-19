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
        self._instance = os.getenv('DEV_SQL_INSTANCE', '')
        self._connection = None
        self._echo = True

        # Check if we are on the production environment and set the values for production
        if 'gunicorn' in os.getenv('SERVER_SOFTWARE', ''):
            self._host = os.getenv('PROD_SQL_SERVER', '')
            self._username = os.getenv('PROD_SQL_USERNAME', '')
            self._password = os.getenv('PROD_SQL_PASSWORD', '')
            self._database = os.getenv('PROD_SQL_DATABASE', '')
            self._instance = os.getenv('PROD_SQL_INSTANCE', '')
            self._connection = None
            self._echo = False

        # Create the connection string that is needed when we create a connection
        self.connection_string = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
            username = self._username,
            password = self._password,
            host = self._host,
            database = self._database
        )

        # For production, we use a socket-connection. This is faster and cheaper
        if 'gunicorn' in os.getenv('SERVER_SOFTWARE', ''):
            self.connection_string = 'mysql+pymysql://{username}:{password}@/{database}?unix_socket=/cloudsql/{instance}'.format(
                username = self._username,
                password = self._password,
                instance = self._instance,
                database = self._database
            )

        # Create a SQLalchemy engine that we can use later on
        self._engine = sqlalchemy.create_engine(
            self.connection_string,
            echo = self._echo,
            pool_pre_ping = True,
            pool_recycle = 300
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
#---------------------------------------------------------------------------------------------------