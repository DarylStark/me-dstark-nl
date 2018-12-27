#---------------------------------------------------------------------------------------------------
# api.py
#
# Date: 2018-12-20
#
# The code for the REST API
#---------------------------------------------------------------------------------------------------
# Global imports
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
import database
#---------------------------------------------------------------------------------------------------
class API:
    """ Class for the REST API of the website """

    def get_venues(self):
        """ API method for '/venues'. Returns all or filtered venues from the database """
        
        # Create a object for database interaction
        db = database.Database()

        # Get the venues
        venues = db.venues()

        # Return the venues in a dict
        # TODO: create better objects for this API
        return {
            'APIResult': {
                'success': True
            },
            'data': [ x.name for x in venues ]
        }
    
    def get_stages(self, venue = None):
        """ API method for '/stges'. Returns all or filtered stages from the database """

        # Create a object for database interaction
        db = database.Database()

        # Get the stages
        stages = db.stages(venue = venue)

        # Return the stages in a dict
        # TODO: create better objects for this API
        return {
            'APIResult': {
                'success': True
            },
            'data': [ x.name for x in stages ]
        }

    def get_events(self):
        """ API method for '/events'. Returns all or filtered events from the database """

        return {
            'APIResult': {
                'success': False
            },
            'data': [ 'yet to be implemented' ]
        }
    
    def sync_events(self, service = None):
        """ API method for '/events.Sync'. Syncs all events for a specific service """

        # Set success to False. We set it to False later on when something happends
        success = True

        # We set events to a empty list so we won't get errors later on
        events = []

        # The API result we are going to return
        data = {
            'new_events': 0,
            'updated_events': 0,
            'errors': 0
        }

        # Check the service that we are going to sync
        if service == 'TivoliVredenburg':
            # Create a object for the eventretriever for TivoliVredenburg and download all the
            # events for this Service
            retriever = eventretriever.EventRetrieverTivoliVredenburg()
            events = retriever.retrieve_events()

        # Create a object for database interaction
        db = database.Database()
        
        # If we have events, sync them with the database
        for event in events:
            retval = db.sync_event(event)

            # Check the return value and update the API result
            if retval == 1:
                # The event existed and was changes
                data['updated_events'] += 1
            elif retval == 0:
                # The event was new
                data['new_events'] += 1
            elif retval == False:
                # Something went wrong during the eent sync
                data['errors'] += 1
            else:
                # The event existed but was not changed
                pass

        return {
            'APIResult': {
                'success': success
            },
            'data': [ data ]
        }
#---------------------------------------------------------------------------------------------------
api = API()
#---------------------------------------------------------------------------------------------------