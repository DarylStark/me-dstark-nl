#!/usr/bin/env python3
"""
    me - page_api_users.py

    API module for '/api/users'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import APIPage
from me import PageAPI
from me_database import *
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('users')
class PageAPIUsers(APIPage):
    """ Class that can be called to run the API for users """

    def __init__(self):
        """ The initiator for this object sets the API endpoints and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API endpoint gets in """
        
        self._api_endpoints = {
            'get': self.get
        }
    
    @PageAPI.api_endpoint(allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get(self, *args, **kwargs):
        """ API method to return users in the database """

        # Create a session with the database
        all_users = list()
        session = Database.session()

        # Get all users from the database
        users = session.query(User).order_by(User.name)
        allusercount = users.count()

        # TODO: Introduce pages and limits
    
        return (users.all(), allusercount)
#---------------------------------------------------------------------------------------------------