#!/usr/bin/env python3
"""
    me - apipage.py

    Base class for API pages
"""
#---------------------------------------------------------------------------------------------------
# Imports
import re
from me import Page
from abc import abstractmethod
from me.exceptions import *
#---------------------------------------------------------------------------------------------------
class APIPage(Page):
    """ Base class for API pages. This class is abstract, meaning that it is impossible to create a
        instance of it """
    
    @abstractmethod
    def __init__(self):
        """ The initiator sets a default empty dict of API endpoints. Each derived class can set its
            own dict with API endpoints. """
        self._api_endpoints = {}

    def show_page(self, path, **kwargs):
        """ When this API group get requested, we have to find the API endpoint that the user is
            trying to get """
        
        # First, find the API endpoint. This will always be the third group in the 'path'. If the
        # 'path' is '/api/events/get', for example, the third part is 'get', which is the API
        # endpoint. We retrieve this information using a regular expression
        endpoint = re.findall('^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+/([a-zA-Z0-9-_]+)', path)
        
        # Check if we got any result
        if len(endpoint) == 1:
            # Check if this API endpoint is somewhere in the local dict '_api_endpoint'
            if endpoint[0] in self._api_endpoints:
                # We got a hit! Lets call the associated method and return its value
                return self._api_endpoints[endpoint[0]](path = path, **kwargs)
            else:
                # If we cannot find the endpoint in the dict, we raise an error
                raise MeAPIEndPointInvalidException('API endpoint "{endpoint}" is not a valid API endpoint in group "{group}"'.format(endpoint = endpoint[0], group = self.group))
        else:
            # If we didn't get any results; raise an error
            raise MeAPINoEndPointException('No API endpoint specified')
#---------------------------------------------------------------------------------------------------