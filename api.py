#---------------------------------------------------------------------------------------------------
# api.py
#
# Date: 2018-12-20
#
# The code for the REST API
#---------------------------------------------------------------------------------------------------
# Global imports
import datetime
import math
import time
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
import database
#---------------------------------------------------------------------------------------------------
class API:
    """ Class for the REST API of the website """

    def create_api_return(self, api, error_code = 0, error_text = '', data = [], length = 0, retval = {}, page = 0, limit = 0, runtime = 0):
        """ Creates the default API return code """
        
        # Calculate the maxpage
        maxpage = 0
        if page > 0 and limit > 0:
            maxpage = int(math.ceil(float(length) / float(limit)))

        # Create the empty object
        api_object = {
            'request': {
                'api': api,
                'runtime': round(runtime, 3)
            },
            'error': {
                'code': error_code,
                'text': error_text
            },
            'data': {
                'data': data,
                'length': length,
                'page': page,
                'maxpage': maxpage,
                'limit': limit,
                'data_len': len(data)
            },
            'retval': retval
        }

        # Return the object
        return api_object

    def get_venues(self):
        """ API method for '/venues'. Returns all or filtered venues from the database """
        
        return self.create_api_return(api = 'venues', error_code = 1, error_text = 'not implemented yet')
    
    def get_stages(self, venue = None):
        """ API method for '/stges'. Returns all or filtered stages from the database """

        return self.create_api_return(api = 'venues', error_code = 1, error_text = 'not implemented yet')

    def get_events(self):
        """ API method for '/events'. Returns all or filtered events from the database """

        return self.create_api_return(api = 'venues', error_code = 1, error_text = 'not implemented yet')
    
    def sync_events(self, service = None):
        """ API method for '/events.Sync'. Syncs all events for a specific service """

        # Get the start time
        time_start = time.time()

        # Set a default error code and text
        error_code = 0
        error_text = ''

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
            # First, try to add the event. If this fails, we find the old event and update it
            session = db._session_factory()

            # Set the Event_Added and Event_Changed to the current date
            event.added = datetime.datetime.utcnow()
            event.changed = datetime.datetime.utcnow()

            # Add the new event
            try:
                # Add the event
                session.add(event)
                session.commit()
                original_id = event.id
                session.close()

                # Add a Feed Item for the new Event
                item = database.FeedItem()
                item.itemtype = item.TYPE_NEW_EVENT
                item.event = original_id
                item.date = datetime.datetime.utcnow()
                item.changedate = datetime.datetime.utcnow()

                # Add the new object
                session = db._session_factory()
                session.add(item)
                session.commit()
                session.close()

                # Increase the counter
                data['new_events'] += 1
            except:
                # The object already existed. Rollback the changes and update the existing object
                session.rollback()
                session.close()

                # Find the original object
                session = db._session_factory()
                original_events = session.query(database.Event).filter(
                    database.Event.unique == event.unique
                )

                # Get the original event
                original_event = original_events[0]
                original_id = original_event.id
                original_tracked = original_event.tracked

                # Update the original event and keep track of the made changes
                attributes = [
                    'title', 'support', 'venue', 'stage',
                    'date', 'price', 'free', 'soldout',
                    'doorsopen', 'starttime', 'url', 'url_tickets',
                    'image'
                ]
                changes = [ db.compare_and_set_attribute(attribute, original_event, event) for attribute in attributes ]

                # Remove all None's from the list
                changes = [ change for change in changes if change is not None ]

                # The original event is now updated with the new info and can be saved
                session.commit()
                session.close()

                # For every change in the event, we create a logentry that can be used later
                eventchange_ids = []
                for change in changes:
                    # Create a EventChange object and fill it with the correct information
                    eventchange = database.EventChange()
                    eventchange.event = original_id
                    eventchange.changed = datetime.datetime.utcnow()
                    eventchange.field = change[0]
                    eventchange.oldvalue = change[1]
                    eventchange.newvalue = change[2]

                    # Add the new object
                    session = db._session_factory()
                    session.add(eventchange)
                    session.commit()

                    # Save the ID of the 'EventChange' in a dict
                    eventchange_ids.append(eventchange.id)

                    # Close the session
                    session.close()

                # Add a new Feed Item for this change
                if original_tracked == 1 or 'support' in [ c[0] for c in changes ]:
                    # Create a object for the FeedItem
                    item = database.FeedItem()
                    item.itemtype = item.TYPE_EVENT_CHANGED
                    item.event = original_id
                    item.date = datetime.datetime.utcnow()
                    item.changedate = datetime.datetime.utcnow()

                    # If the event was tracked, the item has to be different
                    if original_tracked == 1:
                        item.itemtype = item.TYPE_TRACKED_EVENT_CHANGED

                    # Add the new object
                    session = db._session_factory()
                    session.add(item)
                    session.commit()

                    # Save the id
                    item_id = item.id

                    # Close the session
                    session.close()

                    # Add Feed Item Event Changes
                    for change in eventchange_ids:
                        # Create a FeedItemEventChange object
                        itemchange = database.FeedItemEventChange()
                        itemchange.feeditem = item_id
                        itemchange.eventchange = change

                        # Add the new object
                        session = db._session_factory()
                        session.add(itemchange)
                        session.commit()
                        session.close()
                    
                # Increase the counter
                if len(eventchange_ids) > 0:
                    data['updated_events'] += 1
        
        # Get the end time
        time_end = time.time()

        # Return the sync data
        return self.create_api_return(
            api = 'events.Sync',
            error_code = error_code,
            error_text = error_text,
            data = data,
            length = 0,
            retval = {},
            page = 0,
            limit = 0,
            runtime = time_end - time_start
        )
    
    def get_feed(self, limit = 15, page = 1):
        """ API method for '/feed'. Returns all or filtered feeditems from the database """

        # Get the start time
        time_start = time.time()

        # Set a default error code and text
        error_code = 0
        error_text = ''

        # Create default values
        data = []
        length = 0

        try:
            # Create a object for database interaction
            db = database.Database()

            # Get the count of rows in the database
            session = db._session_factory()
            length = session.query(database.FeedItem).add_entity(database.Event).outerjoin(database.Event).count()
            session.close()

            # Get the feeditems for the requested page
            session = db._session_factory()
            feeditems = session.query(database.FeedItem).add_entity(database.Event).outerjoin(database.Event).limit(limit).offset((page - 1) * limit)
            session.close()

            # Create a list with dicts
            for feeditem in feeditems:
                # Create a dict for the feeditem
                item = feeditem.FeedItem.get_dict()

                # If this is a event-type, we have to add the event
                if feeditem.FeedItem.itemtype in (feeditem.FeedItem.TYPE_NEW_EVENT, feeditem.FeedItem.TYPE_TRACKED_EVENT_CHANGED, feeditem.FeedItem.TYPE_EVENT_CHANGED):
                    item['event'] = feeditem.Event.get_dict()
                
                # If this is a event-change, we need to add the changes. We get these from the database
                # seperatly; we don't do this via a JOIN because that would result in more then one
                # 'feed-item'.
                if feeditem.FeedItem.itemtype in (feeditem.FeedItem.TYPE_TRACKED_EVENT_CHANGED, feeditem.FeedItem.TYPE_EVENT_CHANGED):
                    session = db._session_factory()
                    changes = session.query(database.FeedItemEventChange).add_entity(database.EventChange).outerjoin(database.EventChange)
                    session.close()

                    item['changes'] = []
                    for change in changes:
                        item['changes'].append(change.EventChange.get_dict())
                
                # Append the created dict to the list
                data.append(item)
        except:
            error_code = 1
            error_text = 'Unknown error'
        
        # Get the end time
        time_end = time.time()

        # Return the feed
        return self.create_api_return(
            api = 'feed',
            error_code = error_code,
            error_text = error_text,
            data = data,
            length = length,
            retval = {},
            page = page,
            limit = limit,
            runtime = time_end - time_start
        )
#---------------------------------------------------------------------------------------------------
api = API()
#---------------------------------------------------------------------------------------------------