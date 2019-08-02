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
        """ The initiator sets a default empty dict of API calls. Each derviced class can set its
            own dict with API calls. """
        self._api_calls = {}

    def show_page(self, path, **kwargs):
        """ When this API group get requested, we have to find the API call that the user is trying
            to get """
        
        # First, find the API call. This will always be the third group in the 'path'. If the 'path'
        # is '/api/events/get', for example, the third part is 'get', which is the API call. We
        # retrieve this information using a regular expression
        call = re.findall('^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+/([a-zA-Z0-9-_]+)', path)
        
        # Check if we got any result
        if len(call) == 1:
            # Check if this API call is somewhere in the local dict '_api_calls'
            if call[0] in self._api_calls:
                # We got a hit! Lets call the associated method and return its value
                return self._api_calls[call[0]](path = path, **kwargs)
            else:
                # If we cannot find the call in the dict, we raise an error
                raise MeAPIEndPointInvalidException('API call "{call}" is not a valid API call in group "{group}"'.format(call = call[0], group = self.group))
        else:
            # If we didn't get any results; raise an error
            raise MeAPINoEndPointException('No API call specified')
#---------------------------------------------------------------------------------------------------