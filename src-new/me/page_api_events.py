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
    """ Class that can be called to run the API for Events """

    def show_page(self, **kwargs):
        # TODO: Implement and add DOCSTRING
        return 'Welcome to our events'
#---------------------------------------------------------------------------------------------------