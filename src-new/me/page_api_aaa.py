#!/usr/bin/env python3
"""
    me - page_api_aaa.py

    API module for '/api/aaa'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('aaa')
class PageAPIAAA(APIPage):
    """ Class that can be called to run the API for aaa """

    def __init__(self):
        """ The initiator for this object sets the API calls and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API call gets in """
        
        self._api_calls = {
            'verify': self.verify
        }
    
    @PageAPI.api_endpoint
    def verify(self, *args, **kwargs):
        """ Method to verify the credentials of a logging in users """
        return { 'value' : 'verify return' }
#---------------------------------------------------------------------------------------------------