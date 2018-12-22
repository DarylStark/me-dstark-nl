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
        # TODO: remove when we're fully over to ORM
        database.BaseClass.metadata.create_all(self._engine)
    
    def commit(self):
        """ Commits the changes to the database """
        self._session.commit()

    def add_event(self, event):
        """ Adds a event to the database """

        # Add the event and commit the changes
        self._session.add(event)
        self._session.commit()
    
    # TODO: remove when we're fully over to ORM
    def create_schema_old(self):
        """ This method creates the tables when needed """

        # Create an metadata-object
        self._metadata = sqlalchemy.MetaData(bind = self._engine)

        # Create objects for Tables
        self._tables['tEvents'] = sqlalchemy.Table(
            'tEvents',
            self._metadata,
            sqlalchemy.Column('Event_ID', sqlalchemy.Integer, primary_key = True),
            sqlalchemy.Column('Event_Added', sqlalchemy.DateTime, nullable = False),
            sqlalchemy.Column('Event_Changed', sqlalchemy.DateTime, nullable = False),
            sqlalchemy.Column('Event_Tracked', sqlalchemy.Integer, nullable = False),
            sqlalchemy.Column('Event_New', sqlalchemy.Integer, nullable = False),
            sqlalchemy.Column('Event_Title', sqlalchemy.Text, nullable = False),
            sqlalchemy.Column('Event_Support', sqlalchemy.Text),
            sqlalchemy.Column('Event_Venue', sqlalchemy.Text, nullable = False),
            sqlalchemy.Column('Event_Stage', sqlalchemy.Text, nullable = False),
            sqlalchemy.Column('Event_Date', sqlalchemy.Date),
            sqlalchemy.Column('Event_Price', sqlalchemy.Integer),
            sqlalchemy.Column('Event_Free', sqlalchemy.Boolean),
            sqlalchemy.Column('Event_Soldout', sqlalchemy.Boolean),
            sqlalchemy.Column('Event_DoorsOpen', sqlalchemy.Time),
            sqlalchemy.Column('Event_StartTime', sqlalchemy.Time),
            sqlalchemy.Column('Event_URL', sqlalchemy.Text),
            sqlalchemy.Column('Event_URLTickets', sqlalchemy.Text),
            sqlalchemy.Column('Event_Image', sqlalchemy.Text),
            sqlalchemy.Column('Event_Unique', sqlalchemy.Text, nullable = False),
        )

        # Create the schema
        self._metadata.create_all()
#---------------------------------------------------------------------------------------------------