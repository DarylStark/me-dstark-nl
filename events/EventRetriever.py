#---------------------------------------------------------------------------------------------------
# EventRetriever.py
#
# Date: 2018-12-20
#
# Base class for Event Retrievers.
#---------------------------------------------------------------------------------------------------
# Global imports
import requests
import bs4
#---------------------------------------------------------------------------------------------------
# Local imports
from events.Event import Event
#---------------------------------------------------------------------------------------------------
class EventRetriever:
    """ Base class for EventRetrievers. Does basic stuff, like setting the default variables """

    def __init__(self):
        """ Sets default variables for the object """
        self.events = []
#---------------------------------------------------------------------------------------------------