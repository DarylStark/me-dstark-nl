#---------------------------------------------------------------------------------------------------
# EventRetrieverParadiso.py
#
# Date: 2019-01-10
#
# Event Retriever for Paradiso
#---------------------------------------------------------------------------------------------------
# Global imports
import requests
import datetime
import json
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
from database import Event, Stage
#---------------------------------------------------------------------------------------------------
class EventRetrieverParadiso(eventretriever.EventRetriever):
    """ EventRetriever class to retrieve events from the website of Paradiso """

    def retrieve_events(self):
        """ Retrieves all events from the Paradiso website """

        # Set the URL
        url = 'https://api.paradiso.nl/api/events?lang=nl&start_time=now&sort=date&order=asc&limit=30&page={pageindex}&with=locations'
        event_url = 'https://www.paradiso.nl/nl/programma/{slug}/{id}/'
        detail_url = 'https://api.paradiso.nl/api/library/lists/events/{id}?lang=nl'
        image_url = 'https://api.paradiso.nl/img/events/{image}'

        # Set up the loop
        pageindex = 1
        keeplooping = True

        # Start looping through the pages
        while keeplooping:
            # Retrieve the page and get the JSON. We do this in a try block. If we capture an
            # error, we stop. Otherwise; we increase the page and go to the next page with events.
            try:
                # Retrieve the page
                newurl = url.format(pageindex = pageindex)
                page = requests.get(newurl)
                data = page.json()

                # If there is no data, stop processing this page
                if len(data) == 0:
                    raise ValueError

                # Loop through the events on the page
                for event in data:
                    event_object = Event(
                        title = event['title'].split('+')[0].strip(),
                        url = event_url.format(slug = event['slug'], id = str(event['id'])),
                        image = event['main_image__focus_events'],
                        date = datetime.date(
                            int(event['start_date_time'].split()[0].split('-')[0]),
                            int(event['start_date_time'].split()[0].split('-')[1]),
                            int(event['start_date_time'].split()[0].split('-')[2])
                        ),
                        unique = str(event['id']),
                        url_tickets = event['ticket_url'],
                        free = False,
                        soldout = event['sold_out'] == 'option_1',
                        # TODO: make sure this time is in UTC
                        starttime = datetime.datetime.strptime(event['start_date_time'].split()[1], '%H:%M:%S').time()
                    )

                    # Check if there is an support and if there is; fill it
                    splitted_title = event['title'].split('+')
                    if len(splitted_title) > 1:
                        event_object.support = splitted_title[1].strip()

                    # Convert the ticketprice
                    if ',' in event['ticket_price']:
                        event['ticket_price'] = event['ticket_price'].replace(',', '')
                    else:
                        event['ticket_price'] = event['ticket_price'] + '00'
                    
                    event_object.price = int(event['ticket_price'])

                    # Get additional information from the detail_url
                    newurl = detail_url.format(id = str(event['id']))
                    newpage = requests.get(newurl)
                    detaildata = newpage.json()

                    # Check if this event is free
                    try:
                        if detaildata[0]['content']['ticket_price__disabled'] == None:
                            event_object.free = True
                    except:
                        pass

                    try:
                        event = detaildata[0]
                        # TODO: make sure this time is in UTC
                        event_object.doorsopen = datetime.datetime.strptime(event['content']['doors_open__disabled'].split()[1], '%H:%M:%S').time()
                        event_object.image = image_url.format(image = event['content']['main_image__focus_events']['filename'])
                        stagename = event['content']['locations'][0]['content']['title']

                        # Find the stage in the local stagelist
                        if stagename in self.stages.keys():
                            event_object.stage = self.stages[stagename]
                        else:
                            event_object.stage = None
                    except:
                        pass

                    # Add the event to the stack
                    self.events.append(event_object)

                # Increase the pagenumber so th next iteration will do the next page
                pageindex += 1
            except (json.decoder.JSONDecodeError, ValueError):
                # We got an error; stop with the loop
                break
        
        # Return the events
        return self.events
#---------------------------------------------------------------------------------------------------