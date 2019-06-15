#---------------------------------------------------------------------------------------------------
# EventRetrieverZiggoDome.py
#
# Date: 2019-06-13
#
# Event Retriever for Ziggo Dome
#---------------------------------------------------------------------------------------------------
# Global imports
import requests
import bs4
import datetime
import re
import pytz
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
from database import Event, Stage
#---------------------------------------------------------------------------------------------------
class EventRetrieverZiggoDome(eventretriever.EventRetriever):
    """ EventRetriever class to retrieve events from the website of ZiggoDome """

    def __init__(self):
        """ Initiator sets default values """
        super().__init__()

        self.events = []
        self._months = [
            '', 'januari', 'februari', 'maart',
            'april', 'mei', 'juni',
            'juli', 'augustus', 'september',
            'oktober', 'november', 'december'
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
        url = 'https://www.ziggodome.nl/agenda'

        try:
            # Retrieve the page and get the HTML. From this, we can retrieve the URLs
            page = requests.get(url)
            html = str(page.content)

            # Find the stage
            if len(self.stages) > 0:
                stage = self.stages['Ziggo Dome']
            else:
                stage = None

            # Get the URLs
            self.events = [ Event(url = x, unique = x, free = False, stage = stage) for x in re.findall('https://www.ziggodome.nl/event/[0-9]+/[^"]+', html) ]
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
                    title = parsed_page.find('h1', { 'class': 'event_title' }).encode_contents().decode('utf-8')
                    event.title = title
                except AttributeError:
                    event.title = ''
                
                # Find the image for the event
                try:
                    image = parsed_page.find('div', { 'id': 'fallback' })
                    event.image = re.findall('\((.+)\)', image['style'])[0]
                except (AttributeError, KeyError):
                    event.image = None
                
                # Find the date for the event
                try:
                    date = parsed_page.find('h2', { 'class': 'event_date' }).encode_contents().decode('utf-8').split()[1:4]
                    if date[1] in self._months:
                        event.date = datetime.date(
                            int(date[2]),
                            int(self._months.index(date[1])),
                            int(date[0])
                        )
                    else:
                        raise IndexError
                except IndexError:
                    event.date = None
                
                # Find the support act
                try:
                    support = re.findall('<p class="supportact_name">([^<]+)</p>', page.content.decode('utf-8'))[0]
                    event.support = support
                except:
                    event.support = None
                
                # Find the price
                try:
                    price = [ int(x.replace(',', '')) for x in re.findall('Staanplaatsen \(&euro; ([0-9,]+)\)', page.content.decode('utf-8')) ]
                    
                    # If we didn't find anything; try the next method
                    if len(price) == 0:
                        price = [ int(x.replace(',', '')) for x in re.findall('Zitplaatsen \(&euro; ([0-9,]+)\)', page.content.decode('utf-8')) ]
                    
                    # If we didn't find anything; try the next method
                    if len(price) == 0:
                        price = [ int(x.replace(',', '')) for x in re.findall('1e rang \(&euro; ([0-9,]+)\)', page.content.decode('utf-8')) ]
                    
                    # If we didn't find anything; try the next method
                    if len(price) == 0:
                        price = [ int(x.replace(',', '')) for x in re.findall('Veld \(&euro; ([0-9,]+)\)', page.content.decode('utf-8')) ]

                    # If we didn't find anything; try the next method
                    if len(price) == 0:
                        price = [ int(x.replace(',', '')) for x in re.findall('Ring 1 \(&euro; ([0-9,]+)\)', page.content.decode('utf-8')) ]

                    event.price = max(price)
                except:
                    event.price = None
                
                # Find if the event is soldout
                try:
                    if 'Dit concert is uitverkocht' in page.content.decode('utf-8'):
                        event.soldout = True
                    else:
                        event.soldout = False
                except:
                    event.soldout = False
                
                # Find when the doors go open
                try:
                    doors = re.findall('<td>([0-9:]+)</td>.+<td>Deuren open</td>', page.content.decode('utf-8'), flags = re.DOTALL)
                    event.doorsopen = datetime.datetime.strptime(doors[0] + ' +0100', '%H:%M %z').astimezone(pytz.timezone('UTC')).time()
                except:
                    event.doorsopen = None
                
                # Find when the event starts
                try:
                    starttime = re.findall('<td>([0-9:]+)</td>\s+<td>&nbsp;</td>\s+<td>Aanvang show</td>', page.content.decode('utf-8'), flags = re.DOTALL)
                    
                    # If we can't find it, try another way
                    if len(starttime) == 0:
                        starttime = re.findall('<td>([0-9:]+)</td>\s+<td>&nbsp;</td>\s+<td>' + event.title + '</td>', page.content.decode('utf-8'), flags = re.DOTALL)
 
                    event.starttime = datetime.datetime.strptime(starttime[0] + ' +0100', '%H:%M %z').astimezone(pytz.timezone('UTC')).time()
                except:
                    event.starttime = None
                
                # Find the ticket URL
                try:
                    tickets = parsed_page.find('a', { 'title': 'bestel tickets' })
                    event.url_tickets = tickets.get('href')
                except:
                    event.url_tickets = None
#---------------------------------------------------------------------------------------------------