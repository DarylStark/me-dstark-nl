#!/usr/bin/env python3
"""
    me - page_api_users.py

    API module for '/api/users'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
from me_database import *
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
    
    @PageAPI.api_endpoint
    def get(self, *args, **kwargs):
        """ API method to return users in the database """
        
        # Get the users from the database
        retval = ''
        ses = Database.session()
        for a in range(0, 1024):
            users = ses.query(User).order_by(User.name)

            for user in users:
                retval += '<b>{name}</b> ({email})<br />'.format(name = user.name, email = user.email)
        
        ses.close()
        return retval
#---------------------------------------------------------------------------------------------------