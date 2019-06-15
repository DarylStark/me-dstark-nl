#---------------------------------------------------------------------------------------------------
# EventRetrieverEffenaar.py
#
# Date: 2019-06-15
#
# Event Retriever for Effenaar
#---------------------------------------------------------------------------------------------------
# Global imports
import requests
import bs4
import datetime
import re
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
from database import Event, Stage
#---------------------------------------------------------------------------------------------------
class EventRetrieverEffenaar(eventretriever.EventRetriever):
    """ EventRetriever class to retrieve events from the website of Effenaar """

    def __init__(self):
        """ Initiator sets default values """
        super().__init__()

        self.events = []
        self._months = [
            '', 'JANUARY', 'FEBRUARY', 'MARCH',
            'APRIL', 'MAY', 'JUNE',
            'JULY', 'AUGUST', 'SEPTEMBER',
            'OCTOBER', 'NOVEMBER', 'DECEMBER'
        ]

    def retrieve_events(self):
        """ Retrieves all URLs for all events and uses a seperate method to retrieve event
            details """

        # Download a summary of all events from the TivoliVredenburg agenda
        self.retrieve_events_summary()
        
        # Now that we have the summaried for events, let's get all needed information from the
        # detail page of the event
        self.retrieve_event_details()

        # Return the retrieved events
        return self.events
       
    def retrieve_events_summary(self):
        """ Retrieves a summary for the events in the complete agenda """

        # Set the URL
        url = 'https://www.effenaar.nl/agenda'

        try:
            # Retrieve the page and get the HTML. From this, we can retrieve the URLs
            page = requests.get(url)
            html = str(page.content)

            # Get the URLs
            # <a class="overview-title" href="/agenda/9468/ava-luna" data-toggle="tooltip" title="" data-original-title="Weirdo-pop om op te dansen.">Ava Luna</a>
            urls = [ 'https://www.effenaar.nl' + x for x in re.findall('href=\"(\/agenda\/[0-9]+\/[^\"]+)\"', html) ]
            #urls = [ 'https://www.effenaar.nl/agenda/9538/duncanlaurence', 'https://www.effenaar.nl/agenda/9316/queensryche-1', 'https://www.effenaar.nl/agenda/9492/clouseau', 'https://www.effenaar.nl/agenda/9552/kempi-2', 'https://www.effenaar.nl/agenda/9510/nashvillepussy', 'https://www.effenaar.nl/agenda/9219/stahlzeit' ]
            self.events = [ Event(url = x, unique = x, free = False) for x in urls ]
        except:
            pass
    
    def retrieve_event_details(self):
        """ Retrieves event details for the events in the list """

        for event in self.events:
            try:
                # Download the page
                page = requests.get(event.url)
            except requests.exceptions.ConnectionError:
                pass
            else:
                # Parse the HTML that we downloaded
                parsed_page = bs4.BeautifulSoup(page.content, 'html.parser')

                # Find the title for the event
                try:
                    title = parsed_page.find('span', { 'property': 'name' }).encode_contents().decode('utf-8')
                    event.title = title
                except AttributeError:
                    event.title = ''
                
                # Find the image for the event
                try:
                    image = parsed_page.find('img', { 'class': 'spotlight-image js-cutout' }).get('src')
                    event.image = image
                except (AttributeError, KeyError):
                    event.image = None
                
                # Find the date for the event
                try:
                    date = parsed_page.find('time', { 'property': 'startDate' }).get('content').split()
                    month = date[0]
                    day = date[1].replace(',', '')
                    year = date[2]
                    time = date[3]

                    event.date = datetime.date(
                        int(year),
                        int(self._months.index(month.upper())),
                        int(day)
                    )

                    event.starttime = datetime.datetime.strptime(time, '%H:%M').time()
                except IndexError:
                    event.date = None
                
                # Find the support act
                try:
                    support = re.findall('<h2 class=\"spotlight-header-medium\"><span>\+ ([^<]+)<\/span><\/h2>', page.content.decode('utf-8'))[0]
                    event.support = support
                except:
                    event.support = None
                
                # Find the price
                try:
                    price_line = re.findall('<meta property=\"price\" content=\"[^"]+\" \/>', page.content.decode('utf-8'))
                    price = int(re.findall('[0-9]+\.[0-9]+', price_line[0])[0].replace('.', ''))
                    event.price = price
                except:
                    event.price = None
                
                # Find if the event is soldout
                try:
                    soldout = parsed_page.find('span', { 'content': 'SoldOut' })
                    if soldout is None:
                        event.soldout = False
                    else:
                        event.soldout = True
                except:
                    event.soldout = False
                
                # Find when the doors go open
                try:
                    doors = re.findall('<dt>Zaal open</dt>[^<]+<dd>([0-9:]+) uur</dd>', page.content.decode('utf-8'), flags = re.DOTALL)
                    event.doorsopen = datetime.datetime.strptime(doors[0], '%H:%M').time()
                except:
                    event.doorsopen = None
                
                # Find the ticket URL
                try:
                    tickets = re.findall('<a href=\"([^"]+)\" [^>]+>[^T]*Tickets bestellen', page.content.decode('utf-8'), flags = re.DOTALL)[0]
                    event.url_tickets = tickets
                except:
                    event.url_tickets = None
                
                # Find the stage
                try:
                    stage = re.findall('<dt>Locatie</dt>[^<]+<dd>([^<]+)</dd>', page.content.decode('utf-8'), flags = re.DOTALL)[0]
                    # Find the stage in the local stagelist
                    if stage in self.stages.keys():
                        event.stage = self.stages[stage]
                    else:
                        event.stage = None
                except:
                    event.stage = None
#---------------------------------------------------------------------------------------------------