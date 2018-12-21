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
#---------------------------------------------------------------------------------------------------
# Local imports
#---------------------------------------------------------------------------------------------------
class Database:
    """ Class to open database connections and retrieve information from the database """

    def __init__(self):
        """ Sets default variables """

        # Set the Development credentials
        self._host = os.getenv('DEV_SQL_SERVER', '')
        self._username = os.getenv('DEV_SQL_USERNAME', '')
        self._password = os.getenv('DEV_SQL_PASSWORD', '')
        self._database = os.getenv('DEV_SQL_DATABASE', '')
        self._connection = None

        # Check if we are on the production environment and set the values for production
        if 'gunicorn' in os.getenv('SERVER_SOFTWARE', ''):
            self._host = os.getenv('DEV_SQL_SERVER', '')
            self._username = os.getenv('DEV_SQL_USERNAME', '')
            self._password = os.getenv('DEV_SQL_PASSWORD', '')
            self._database = os.getenv('DEV_SQL_DATABASE', '')
            self._connection = None

        # Create the connection string that is needed when we create a connection
        self.connection_string = 'mysql://{username}:{password}@{host}/{database}'.format(
            username = self._username,
            password = self._password,
            host = self._host,
            database = self._database
        )
#---------------------------------------------------------------------------------------------------