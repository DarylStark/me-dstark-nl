#!/usr/bin/env python3
"""
    me - page_api_feed.py

    API module for '/api/feed'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('feed')
class PageAPIFeed(APIPage):
    """ Class that can be called to run the API for the feed """

    def __init__(self):
        """ The initiator for this object sets the API calls and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API call gets in """
        
        self._api_calls = {
            'get': self.get
        }
    
    def get(self, path, **kwargs):
        return 'Getting some feed info?'
#---------------------------------------------------------------------------------------------------