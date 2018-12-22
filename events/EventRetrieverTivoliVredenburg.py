#---------------------------------------------------------------------------------------------------
# EventRetriever.py
#
# Date: 2018-12-20
#
# Event Retriever for TivoliVredenburg
#---------------------------------------------------------------------------------------------------
# Global imports
import requests
import bs4
import datetime
import re
#---------------------------------------------------------------------------------------------------
# Local imports
import events
from database import Event
#---------------------------------------------------------------------------------------------------
class EventRetrieverTivoliVredenburg(events.EventRetriever):
    """ EventRetriever class to retrieve events from the website of TivoliVredenburg """

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
        url = 'https://www.tivolivredenburg.nl/wp-admin/admin-ajax.php?action=get_events&page={pageindex}'

        # Set up the loop
        pageindex = 1
        keeplooping = True

        # Start looping through the pages
        while keeplooping:
            try:
                # Retrieve the page and get the JSON
                newurl = url.format(pageindex = pageindex)
                page = requests.get(newurl)
                data = page.json()

                # Loop through the events we received
                for event in data:
                    # Create a new Event object with the properties we already have. We will add
                    # details for his event later. The 'day' attribute in the TivoliVredenburg
                    # output is in the form of 'di 3', so we have to strip off the first part.
                    event_object = Event(
                        title = event['title'],
                        url = event['link'],
                        image = event['image'],
                        date = datetime.datetime(
                            int(event['year']),
                            int(event['yearMonth'][4:]),
                            int(event['day'].split()[-1])
                        ),
                        venue = 'TivoliVredenburg',
                        unique = event['link']
                    )

                    # Add the event to the stack
                    self.events.append(event_object)

                # Increase the page counter
                pageindex += 1
            except TypeError:
                # When we receive a TypeError, it is very likely we reached the last page. We can
                # stop the loop now! We're done!
                break
    
    def retrieve_event_details(self):
        """ Retrieves event details for the events in the database """

        # Loop over the events in the object and open the URL in the Event. Retrieve extra details
        # from the event from that page and set it in the Event
        for event in self.events:
            # Download the page and parse the HTML
            page = requests.get(event.url)

            # Parse the HTML that we downloaded
            parsed_page = bs4.BeautifulSoup(page.content, 'html.parser')

            # Find the support act
            try:
                supportact = parsed_page.find('span', string = 'support').parent.find_next_sibling().find('span').text.strip()
                event.supportact = supportact
            except AttributeError:
                event.supportact = None
            
            # Find an image. There is already an image in there from the summary, but the images on
            # the detailpage are in much higher resolution. If we don't find any, we don't change
            # the image as it is now, so we get the summary image only if we can't find any bigger
            # on the detail page
            try:
                # Find all images on the page and use only the first one. The first one is the big
                # image used for the event.
                image = parsed_page.find_all('img')[0].get('src')
                event.image = image
            except (AttributeError, IndexError):
                pass
            
            # Find the price for the event
            try:
                # Find the element with the price
                price_html = str(parsed_page.find('div', { 'class': 'price right' }))

                # Extract the price from that
                regex_price = re.compile('</span>([^<]*)<')
                price = regex_price.findall(price_html)[0].strip()

                # Remove clutter
                price = price.replace(',-', ',00') \
                             .replace(',', '')
                
                # Set the price in the object
                event.price = int(price)
            except (AttributeError, ValueError, IndexError):
                event.price = None

            # Check if the concert if Free
            try:
                # Find the 'free' element on the page (if there is any)
                free = parsed_page.find('span', string = 'Gratis')
                if not free is None:
                    event.free = True
                else:
                    event.free = False
            except:
                event.free = None
            
            # Check if the event is sold out
            try:
                # Find the 'soldout' element on the page (if there is any)
                soldout = parsed_page.find('span', string = 'Uitverkocht')
                event.soldout = not soldout is None
                #if not soldout is None:
                #    event.soldout = True
                #else:
                #    event.soldout = False
            except:
                event.soldout = None
            
            # Find the time the doors open
            try:
                doorsopen = parsed_page.find('span', string = 'zaal open').parent.find_next_sibling().find('span').text.strip()
                event.timedoorsopen = datetime.datetime.strptime(doorsopen, '%H:%M').time()
            except AttributeError:
                event.doorsopen = None
            
            # Find the time the event starts
            try:
                start = parsed_page.find('span', string = 'aanvang').parent.find_next_sibling().find('span').text.strip()
                event.timestart = datetime.datetime.strptime(start, '%H:%M').time()
            except AttributeError:
                event.doorsopen = None

            # Find the URL to buy tickets
            try:
                tickets = parsed_page.find('a', { 'class': 'order-tickets' })
                event.url_tickets = tickets.get('href')
            except AttributeError:
                event.doorsopen = None
#---------------------------------------------------------------------------------------------------