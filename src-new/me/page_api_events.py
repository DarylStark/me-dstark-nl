#!/usr/bin/env python3
"""
    me - page_api_events.py

    API module for '/api/events'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('events')
class PageAPIEvents(APIPage):
    """ Class that can be called to run the API for events """

    def __init__(self):
        """ The initiator for this object sets the API calls and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API call gets in """
        
        self._api_calls = {
            'get': self.get
        }
    
    def get(self, path, **kwargs):
        return 'Getting some event info?'
#---------------------------------------------------------------------------------------------------