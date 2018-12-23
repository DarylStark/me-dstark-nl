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
        return {
            'APIResult': {
                'success': True
            },
            'data': [ x.name for x in venues ]
        }

    def get_events(self):
        """ API method for '/events'. Returns all or filtered events from the database """

        return {
            'APIResult': {
                'success': False
            },
            'data': [ 'yet to be implemented' ]
        }
#---------------------------------------------------------------------------------------------------
api = API()
#---------------------------------------------------------------------------------------------------