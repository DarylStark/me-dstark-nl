#!/usr/bin/env python3
"""
    me - page_api_users.py

    API module for '/api/users'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('users')
class PageAPIUsers(APIPage):
    """ Class that can be called to run the API for users """

    def __init__(self):
        """ The initiator for this object sets the API calls and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API call gets in """
        
        self._api_calls = {
            'get': self.get
        }
    
    def get(self, path, **kwargs):
        """ API method to return users in the database """
        return '[ users ]'
#---------------------------------------------------------------------------------------------------