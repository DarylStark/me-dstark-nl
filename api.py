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
import os
import sqlalchemy
import flask
from flask import request
from flask import session as flasksession
from google.oauth2 import id_token
from google.auth.transport import requests
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
import database
from is_logged_in import is_logged_in
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
    
    def verify_user(self):
        """ API method for 'user.Verify'. Verifies a user login from Google """

        # Get the start time
        time_start = time.time()

        # Destroy the session
        flasksession.clear()

        # Set a default error code and text
        error_code = 0
        error_text = ''

        # False retval
        retval = {
            'loggedin': False,
            'name': None
        }

        # Default values
        valid = False

        # Get the data in the request
        token = request.form.get('token')

        # Get token and check validity
        # TODO: move the Client ID to the app.yaml file
        try:
            # Get the idinfo for this session
            client_id = '167809871556-5rtenoj1e65tic5nu08m6g197e4dm9d1.apps.googleusercontent.com'
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

            # Check if the token is signed correctly
            if idinfo['iss'] not in [ 'accounts.google.com', 'https://accounts.google.com' ]:
                error_code = 1
                error_text = 'This aint a correct Google User'
                raise ValueError()
            
            # Get the account ID and the e-mailadress
            user_id = idinfo['sub']
            user_email = idinfo['email']
            user_name = idinfo['name']
            user_image = idinfo['picture']

            # Check if there is a profile for this user. If there is, allow him to login, otherwise
            # raise a ValueError so the user cannot login

            # Create a object for database interaction
            db = database.Database()

            # Create a session and look for the user, based on emailaddress
            session = db._session_factory()
            user = session.query(
                database.User
            ).filter(
                database.User.email == user_email
            )

            # Check if we got something
            if user.count() == 1:
                # Set valid to True so the client knows to login
                valid = True

                # Set the username in the return value so the client can do something with it
                retval['name'] = user_name

                # Update the record in the database
                user[0].name = user_name
                user[0].google_id = user_id
                user[0].image = user_image

                # Write to the database
                session.commit()

                # Close the session
                session.close()
            else:
                session.close()
                error_code = 2
                error_text = 'User is not allowed to log in'
                raise ValueError()
        except ValueError:
            # Invalid token
            valid = False

        # Create the correct return value and start a session if possible
        if valid:
            flasksession['loggedin'] = True
            retval['loggedin'] = True
        else:
            retval['loggedin'] = False

        # Get the end time
        time_end = time.time()

        # Return the sync data
        return self.create_api_return(
            api = 'user.Verify',
            error_code = error_code,
            error_text = error_text,
            runtime = time_end - time_start,
            retval = retval
        )
    
    def sync_events(self, service = None):
        """ API method for '/events.Sync'. Syncs all events for a specific service """

        # Check if we can run the API. We can either run it when the user is logged in, or when
        # GAE starts it as cronjob. For the latter, we don't need to be logged in
        logged_in = is_logged_in()
        cronjob = request.headers.get('X-Appengine-Cron') == 'true' and request.remote_addr == '10.0.0.1'

        if logged_in or cronjob:
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create a object for database interaction
            db = database.Database()

            # Get all stages from the database
            stagelist = {}
            session = db._session_factory()
            stages = session.query(
                database.Stage
            ).add_entity(
                database.Venue
            ).join(
                database.Venue
            )

            # Add the stages to the stagelist
            for stage in stages:
                if stage.Venue.name in stagelist.keys():
                    stagelist[stage.Venue.name][stage.Stage.name] = stage.Stage.id
                else:
                    stagelist[stage.Venue.name] = { stage.Stage.name: stage.Stage.id }

            # Close the session
            session.close()

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
                if 'TivoliVredenburg' in stagelist.keys():
                    retriever.set_stages(stagelist['TivoliVredenburg'])
                events = retriever.retrieve_events()

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
                        'title', 'support', 'stage',
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
                    if len(changes) > 0 and (original_tracked > 0 or 'support' in [ c[0] for c in changes ]):
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
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)
    
    def settracked_event(self, id):
        """ API method for '/events.SetTracked'. Sets a event to tracked """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create the return value
            retval = {
                'id': id,
                'settracked': False
            },

            try:
                # Create a object for database interaction
                db = database.Database()

                # Find the item
                session = db._session_factory()
                item = session.query(
                    database.Event
                ).filter(
                    database.Event.id == id
                ).filter(
                    sqlalchemy.or_(database.Event.tracked == 0, database.Event.tracked == 2)
                )

                if item.count() == 1:
                    # Dismiss the item
                    item[0].changedate = datetime.datetime.utcnow()
                    item[0].tracked = 1
                    session.commit()

                    # Create the return value
                    retval = {
                        'id': id,
                        'settracked': True
                    },
                else:
                    # Not found, return an error
                    error_code = 1
                    error_text = 'Item cannot be found or is already tracked'

                    # Create the return value
                    retval = {
                        'id': id,
                        'settracked': False
                    },
            except:
                # Unknown error happend
                error_code = 2
                error_text = 'Unknown error happened'

            # Get the end time
            time_end = time.time()

            # Return the feed
            return self.create_api_return(
                api = 'events.SetTracked',
                error_code = error_code,
                error_text = error_text,
                retval = retval,
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)

    def setnottracked_event(self, id):
        """ API method for '/events.SetNotTracked'. Sets a event to not tracked """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create the return value
            retval = {
                'id': id,
                'setnottracked': False
            },

            try:
                # Create a object for database interaction
                db = database.Database()

                # Find the item
                session = db._session_factory()
                item = session.query(
                    database.Event
                ).filter(
                    database.Event.id == id
                ).filter(
                    sqlalchemy.or_(database.Event.tracked == 1, database.Event.tracked == 2)
                )

                if item.count() == 1:
                    # Dismiss the item
                    item[0].changedate = datetime.datetime.utcnow()
                    item[0].tracked = 0
                    session.commit()

                    # Create the return value
                    retval = {
                        'id': id,
                        'setnottracked': True
                    },
                else:
                    # Not found, return an error
                    error_code = 1
                    error_text = 'Item cannot be found or is already not tracked'

                    # Create the return value
                    retval = {
                        'id': id,
                        'setnottracked': False
                    },
            except:
                # Unknown error happend
                error_code = 2
                error_text = 'Unknown error happened'

            # Get the end time
            time_end = time.time()

            # Return the feed
            return self.create_api_return(
                api = 'events.SetNotTracked',
                error_code = error_code,
                error_text = error_text,
                retval = retval,
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)

    def setgoing_event(self, id):
        """ API method for '/events.SetGoing'. Sets a event to going """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create the return value
            retval = {
                'id': id,
                'setgoing': False
            },

            try:
                # Create a object for database interaction
                db = database.Database()

                # Find the item
                session = db._session_factory()
                item = session.query(
                    database.Event
                ).filter(
                    database.Event.id == id
                ).filter(
                    sqlalchemy.or_(database.Event.tracked == 0, database.Event.tracked == 1)
                )

                if item.count() == 1:
                    # Dismiss the item
                    item[0].changedate = datetime.datetime.utcnow()
                    item[0].tracked = 2
                    session.commit()

                    # Create the return value
                    retval = {
                        'id': id,
                        'setgoing': True
                    },
                else:
                    # Not found, return an error
                    error_code = 1
                    error_text = 'Item cannot be found or is already tracked'

                    # Create the return value
                    retval = {
                        'id': id,
                        'setgoing': False
                    },
            except:
                # Unknown error happend
                error_code = 2
                error_text = 'Unknown error happened'

            # Get the end time
            time_end = time.time()

            # Return the feed
            return self.create_api_return(
                api = 'events.SetGoing',
                error_code = error_code,
                error_text = error_text,
                retval = retval,
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)
    
    def get_events(self, limit = 15, page = 1, tracked = None, date = None):
        """ API method for '/events.Get'. Returns all or filtered events from the database """

        if is_logged_in():
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
                query = session.query(
                    database.Event
                ).add_entity(
                    database.Stage
                ).add_entity(
                    database.Venue
                ).outerjoin(
                    database.Stage
                ).outerjoin(
                    database.Venue
                )

                # Add the filters, when needed
                if tracked is not None:
                    query = query.filter(
                        database.Event.tracked == tracked
                    )
                
                if date is not None:
                    query = query.filter(
                        database.Event.date == date
                    )

                # Create one query for the length
                length = query.count()

                # And one for the events
                events = query.limit(
                    limit
                ).offset(
                    (page - 1) * limit
                )

                # Close the session
                session.close()

                # Create a list with dicts
                for event in events:
                    # Create a dict for the feeditem
                    item = event.Event.get_dict()
                    
                    # Add a empty stage
                    item['stage'] = {
                        'stage': None,
                        'venue': None
                    }

                    # Add the venue
                    if event.Event.stage:
                        item['stage'] = {
                            'stage': event.Stage.name,
                            'venue': event.Venue.name
                        }
                    
                    # Append the created dict to the list
                    data.append(item)
            except:
                error_code = 1
                error_text = 'Unknown error'

            # Get the end time
            time_end = time.time()

            # Return the feed
            return self.create_api_return(
                api = 'events.Get',
                error_code = error_code,
                error_text = error_text,
                data = data,
                length = length,
                page = page,
                limit = limit,
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)

    def get_feed(self, limit = 15, page = 1, dismissed = 0):
        """ API method for '/feed.Get'. Returns all or filtered feeditems from the database """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create default values
            data = []
            length = 0

            # Check the dismissed status and transform it to the correct status
            status = 1
            if dismissed > 0:
                status = 2

            try:
                # Create a object for database interaction
                db = database.Database()

                # Get the count of rows in the database
                session = db._session_factory()
                length = session.query(
                    database.FeedItem
                ).add_entity(
                    database.Event
                ).add_entity(
                    database.Stage
                ).add_entity(
                    database.Venue
                ).outerjoin(
                    database.Event
                ).outerjoin(
                    database.Stage
                ).outerjoin(
                    database.Venue
                ).filter(
                    database.FeedItem.status == status
                ).count()
                session.close()

                # Get the feeditems for the requested page
                session = db._session_factory()
                feeditems = session.query(
                    database.FeedItem
                ).add_entity(
                    database.Event
                ).add_entity(
                    database.Stage
                ).add_entity(
                    database.Venue
                ).outerjoin(
                    database.Event
                ).outerjoin(
                    database.Stage
                ).outerjoin(
                    database.Venue
                ).filter(
                    database.FeedItem.status == status
                ).order_by(
                    database.FeedItem.changedate.desc(),
                    database.FeedItem.date.desc(),
                    database.FeedItem.id.desc()
                ).limit(
                    limit
                ).offset(
                    (page - 1) * limit
                )
                session.close()

                # Create a list with dicts
                for feeditem in feeditems:
                    # Create a dict for the feeditem
                    item = feeditem.FeedItem.get_dict()

                    # If this is a event-type, we have to add the event
                    if feeditem.FeedItem.itemtype in (feeditem.FeedItem.TYPE_NEW_EVENT, feeditem.FeedItem.TYPE_TRACKED_EVENT_CHANGED, feeditem.FeedItem.TYPE_EVENT_CHANGED):
                        item['event'] = feeditem.Event.get_dict()

                        # Create empty stage fields
                        stagefields = {
                            'stage': None,
                            'venue': None
                        }
                    
                        # If the event has a stage, we have to fill in the fields
                        if feeditem.Event.stage:
                            stagefields = {
                                'stage': feeditem.Stage.name,
                                'venue': feeditem.Venue.name
                            }
                        
                        # Add the stagefields to the event
                        item['event']['stage'] = stagefields
                    
                    # If this is a event-change, we need to add the changes. We get these from the database
                    # seperatly; we don't do this via a JOIN because that would result in more then one
                    # 'feed-item'.
                    if feeditem.FeedItem.itemtype in (feeditem.FeedItem.TYPE_TRACKED_EVENT_CHANGED, feeditem.FeedItem.TYPE_EVENT_CHANGED):
                        session = db._session_factory()
                        changes = session.query(
                            database.FeedItemEventChange
                        ).add_entity(
                            database.EventChange
                        ).outerjoin(
                            database.EventChange
                        ).filter(
                            database.FeedItemEventChange.feeditem == feeditem.FeedItem.id
                        )
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
                api = 'feed.Get',
                error_code = error_code,
                error_text = error_text,
                data = data,
                length = length,
                page = page,
                limit = limit,
                runtime = time_end - time_start
            )
        else:
            flask.abort(403)
    
    def dismiss_feed(self, id):
        """ API method for '/feed.Dismiss'. Dismisses a feeditem """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create the return value
            retval = {
                'id': id,
                'dismissed': False
            },

            try:
                # Create a object for database interaction
                db = database.Database()

                # Find the item
                session = db._session_factory()
                item = session.query(
                    database.FeedItem
                ).filter(
                    database.FeedItem.id == id
                ).filter(
                    database.FeedItem.status == 1
                )

                if item.count() == 1:
                    # Dismiss the item
                    item[0].changedate = datetime.datetime.utcnow()
                    item[0].status = 2
                    session.commit()

                    # Create the return value
                    retval = {
                        'id': id,
                        'dismissed': True
                    },
                else:
                    # Not found, return an error
                    error_code = 1
                    error_text = 'Item cannot be found or is already dismissed'

                    # Create the return value
                    retval = {
                        'id': id,
                        'dismissed': False
                    },
            except:
                # Unknown error happend
                error_code = 2
                error_text = 'Unknown error happened'

            # Close the session
            session.close()

            # Get the end time
            time_end = time.time()

            # Return the feed
            return self.create_api_return(
                api = 'feed.Dismiss',
                error_code = error_code,
                error_text = error_text,
                retval = retval,
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)

    def setnew_feed(self, id):
        """ API method for '/feed.SetNew'. Undismisses a feeditem """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create the return value
            retval = {
                'id': id,
                'undismissed': False
            },

            try:
                # Create a object for database interaction
                db = database.Database()

                # Find the item
                session = db._session_factory()
                item = session.query(
                    database.FeedItem
                ).filter(
                    database.FeedItem.id == id
                ).filter(
                    database.FeedItem.status == 2
                )

                if item.count() == 1:
                    # Dismiss the item
                    item[0].changedate = datetime.datetime.utcnow()
                    item[0].status = 1
                    session.commit()

                    # Create the return value
                    retval = {
                        'id': id,
                        'undismissed': True
                    },
                else:
                    # Not found, return an error
                    error_code = 1
                    error_text = 'Item cannot be found or is not dismissed'

                    # Create the return value
                    retval = {
                        'id': id,
                        'undismissed': False
                    },
            except:
                # Unknown error happend
                error_code = 2
                error_text = 'Unknown error happened'

            # Close the session
            session.close()

            # Get the end time
            time_end = time.time()

            # Return the feed
            return self.create_api_return(
                api = 'feed.SetNew',
                error_code = error_code,
                error_text = error_text,
                retval = retval,
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)

    def get_template(self, template):
        """ API method for '/template.Get'. Returns a requested template """

        if is_logged_in():
            # Get the start time
            time_start = time.time()

            # Get the end time
            time_end = time.time()

            # Set a default error code and text
            error_code = 0
            error_text = ''

            # Create default values
            data = []

            # Get the template directory and file
            htmldir = 'templates/'
            templatefile = htmldir + template + '.html'

            # Load the templatefile
            with open(templatefile) as tpl:
                data = tpl.read()
                tpl.close()
                data = [ data ]

            # Return the feed
            return self.create_api_return(
                api = 'template.Get',
                error_code = error_code,
                error_text = error_text,
                data = data,
                length = len(data),
                runtime = time_end - time_start
            )
        else:
	        flask.abort(403)
#---------------------------------------------------------------------------------------------------
api = API()
#---------------------------------------------------------------------------------------------------