#---------------------------------------------------------------------------------------------------
# EventRetrieverAfasLive.py
#
# Date: 2019-01-11
#
# Event Retriever for Paradiso
#---------------------------------------------------------------------------------------------------
# Global imports
import requests
import bs4
import datetime
import json
import re
#---------------------------------------------------------------------------------------------------
# Local imports
import eventretriever
from database import Event, Stage
#---------------------------------------------------------------------------------------------------
class EventRetrieverAfasLive(eventretriever.EventRetriever):
    """ EventRetriever class to retrieve events from the website of Afas Live """

    def retrieve_events(self):
        """ Retrieves all events from the Paradiso website """

        # Set the URL
        url = 'https://www.afaslive.nl/agenda/p{pageindex}'

        # Set up the loop
        pageindex = 1
        keeplooping = True
        lastpage = ''

        # Start looping through the pages
        while keeplooping:
            # Retrieve the page and get the JSON. We do this in a try block. If we capture an
            # error, we stop. Otherwise; we increase the page and go to the next page with events.
            try:
                # Retrieve the page
                newurl = url.format(pageindex = pageindex)
                page = requests.get(newurl)

                # Check if the same as the last one, this is the last page. Raise an error. If this
                # is more then page 25, we stop too. This to prevent endless loops if something went
                # wrong
                if str(page.content) == lastpage or pageindex > 24:
                    raise IndexError
                else:
                    # Not the last page! Get all links to events
                    lastpage = str(page.content)
                    concerturls = re.findall('"(https://www.afaslive.nl/agenda/.+?)"', str(lastpage))

                    # Loop through the pages
                    for url in concerturls:
                        # Skip the agenda pages; only event pages allowed!
                        if not re.match('^https://www.afaslive.nl/agenda/p[0-9]{1,3}$', url):
                            # Download the page
                            page = requests.get(url)
                            parsed_page = bs4.BeautifulSoup(page.content, 'html.parser')

                            # Create a object for the event
                            event_object = Event(
                                unique = url,
                                url = url
                            )

                            # Find the title
                            try:
                                event_object.title = parsed_page.find('h1').text.strip()
                            except:
                                event_object.title = None
                            
                            # Find the support act
                            try:
                                event_object.support = parsed_page.find('time', string = 'Support act').find_next_sibling().text.strip()
                            except:
                                event_object.support = None
                            
                            # Find the event date
                            try:
                                date = str(parsed_page.find('p', { 'class': 'meta' }).text.strip())
                                event_object.date = datetime.date(
                                    int(date.split('/')[3].strip()[0:4]),
                                    int(date.split('/')[2].strip()),
                                    int(date.split('/')[1].strip())
                                )
                            except:
                                event_object.date = None
                            
                            # Find the ticket URL
                            try:
                                event_object.url_tickets = parsed_page.find('a', string = 'Bestel tickets').get('href')
                            except:
                                event_object.url_tickets = None
                            
                            # Find if the concert is sold out
                            try:
                                soldout = parsed_page.find('span', { 'class': 'soldout' })
                                if soldout:
                                    event_object.soldout = True
                                else:
                                    event_object.soldout = False
                            except:
                                pass
                            
                            # Find the times for the event
                            try:
                                # Get all 'p' with the times
                                times = parsed_page.findAll('p', { 'class': 'align-mid' })
                                alltimes = []

                                # Find all span's in the p's
                                for time in times:
                                   alltimes.append(time.find('span').text.strip().replace(' uur', ''))

                                # Set the times in the object
                                if re.match('[0-9]{2}:[0-9]{2}', alltimes[0]):
                                    event_object.doorsopen = datetime.datetime.strptime(alltimes[0], '%H:%M').time()
                                if re.match('[0-9]{2}:[0-9]{2}', alltimes[1]):
                                    event_object.starttime = datetime.datetime.strptime(alltimes[1], '%H:%M').time()
                            except:
                                pass
                            
                            # Find the image for the event
                            try:
                                image = parsed_page.find('figure').find('img').get('src')
                                event_object.image = image
                            except:
                                pass
                            
                            # Find the prices
                            try:
                                # Get all 'spans' with the in the 'div' with class 'mid'
                                prices = parsed_page.find('div', { 'class': 'mid' }).findAll('span')

                                # Afas Live has multiple prices, so we collect them all and get the
                                # highest
                                total = []

                                for price in prices:
                                    price = price.text
                                    price = price.replace(',', '')
                                    price = price.replace('.', '')
                                    price = price.replace('€ ', '')
                                    price = price.replace('&euro; ', '')
                                    price = price.replace(' ', '')
                                    total += [ int(price) ]
                                
                                # And we get the average price
                                price = max(total)

                                # The average price will be the price for the event
                                event_object.price = price
                            except:
                                pass
                            
                            # There are no free concerts in Afas Live
                            event_object.free = False

                            # Set the stage (only one possible as far as I know)
                            if 'Black Box' in self.stages.keys():
                                event_object.stage = self.stages['Black Box']

                            # Add the event to the stack
                            self.events.append(event_object)

                # Increase the pagenumber so th next iteration will do the next page
                pageindex += 1
            except IndexError:
                # We got an error; stop with the loop
                break
        
        # Return the events
        return self.events
#---------------------------------------------------------------------------------------------------