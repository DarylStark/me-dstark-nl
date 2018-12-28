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

    def add_event(self, event):
        """ Adds a event to the database """

        # Set the Event_Added and Event_Changed to the current date
        event.added = datetime.datetime.utcnow()
        event.changed = datetime.datetime.utcnow()

        try:
            # Add the event and commit the changes
            session = self._session_factory()
            session.add(event)
            session.commit()

            # Everything went fine, return True
            return event.id, event
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
            # When something goes wrong, do a rollback and return False so the caller can do a new
            # action. Note; if we don't do a rollback, the transaction will stay in place and the
            # next commit will fail too. So we always have to do a rollback!
            session.rollback()
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
            return attribute, var_a, var_b
        
        # They were the same, return None
        return None
    
    def sync_event(self, event):
        """ Checks if a event is already in the database. If it is, it updates it. If it isn't, it
            adds the event using the add_event method of this class. Returns True when the object
            was added. Returns False when something went wrong. Returns a list with changed
            properties when the object already existed. """
        
        # Create an dict to return later
        returnvalue = {
            'action': '',
            'event': None,
            'changes': []
        }
        
        # First, try to add the event. If it succeeds, we are done. If it doesn't succeed, the
        # object is already in the database and we can search for the original one
        add = self.add_event(event)
        if add == False:
            try:
                # Find the original event
                session = self._session_factory()
                original_events = session.query(database.Event).filter(
                    database.Event.unique == event.unique
                )

                # Get the original event
                original_event = original_events[0]

                # Set the ID of the original event for the return value
                returnvalue['event'] = original_event

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

                    # Loop through the changes and create a EventChange object for them
                    for attributechange in changes:
                        newchange = database.EventChange()
                        newchange.event = original_event.id
                        newchange.field = attributechange[0]
                        newchange.oldvalue = attributechange[1]
                        newchange.newvalue = attributechange[2]
                        self.add_event_change(newchange)
                        returnvalue['changes'].append(newchange)
                    
                # Commit the new changes
                session.commit()

                if len(changes) > 0:
                    # We updated the record
                    returnvalue['action'] = 'updated'
                    return returnvalue
                else:
                    # We didn't do anything to the record
                    returnvalue['action'] = 'existed'
                    return returnvalue
            except:
                # Something went wrong, return False
                return False
        else:
            # The event was added; set the ID of the return value
            returnvalue['event'] = add[1]

        # The event was added
        returnvalue['action'] = 'added'

        # Return the value
        return returnvalue
    
    #-----------------------------------------------------------------------------------------------
    # Methods for event changes
    #-----------------------------------------------------------------------------------------------

    def add_event_change(self, event_change):
        """ Adds a event change to the database """

        try:
            # Set the date in the event change
            event_change.changed = datetime.datetime.utcnow()

            # Add the event change and commit the changes
            session = self._session_factory()
            session.add(event_change)
            session.commit()

            # Everything went fine, return True
            return event_change.id, event_change
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
            # When something goes wrong, do a rollback and return False so the caller can do a new
            # action. Note; if we don't do a rollback, the transaction will stay in place and the
            # next commit will fail too. So we always have to do a rollback!
            session.rollback()
            return False
    
    #-----------------------------------------------------------------------------------------------
    # Methods for feed items
    #-----------------------------------------------------------------------------------------------

    def add_feed_item(self, feed_item):
        """ Adds a feed item to the database """

        try:
            # Set the date in the feed item change and add
            feed_item.date = datetime.datetime.utcnow()
            feed_item.changedate = datetime.datetime.utcnow()

            # Add the event change and commit the changes
            session = self._session_factory()
            session.add(feed_item)
            session.commit()

            # Everything went fine, return True
            return feed_item.id, feed_item
        #except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
        except KeyboardInterrupt:
            # When something goes wrong, do a rollback and return False so the caller can do a new
            # action. Note; if we don't do a rollback, the transaction will stay in place and the
            # next commit will fail too. So we always have to do a rollback!
            session.rollback()
            return False
    
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

    def add_feed_item_event_change(self, feeditemeeventchange):
        """ Adds a FeedItemEventChange to the database """

        try:
            # Add the feed item event change and commit the changes
            session = self._session_factory()
            session.add(feeditemeeventchange)
            session.commit()

            # Everything went fine, return True
            return feeditemeeventchange.id, feeditemeeventchange
        #except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
        except KeyboardInterrupt:
            # When something goes wrong, do a rollback and return False so the caller can do a new
            # action. Note; if we don't do a rollback, the transaction will stay in place and the
            # next commit will fail too. So we always have to do a rollback!
            session.rollback()
            return False
    
    def feed_item_event_changes(self, feeditem = None):
        """ Returns the feeditemeventchanges from the database, filtered if needed """

        # Get the feeditemseventchanges from the database, filtered on the requested feeditem
        session = self._session_factory()
        changes = session.query(database.FeedItemEventChange).add_entity(database.EventChange).outerjoin(database.EventChange)

        # Return the result
        return changes
#---------------------------------------------------------------------------------------------------