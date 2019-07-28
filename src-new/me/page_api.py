#!/usr/bin/env python3
"""
    me - page_aapi.py

    Class for the REST API of the application.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import Page
#---------------------------------------------------------------------------------------------------
@Me.register_url(name = 'api', regex = 'api/.*')
class PageAPI(Page):
    """ Class for the REST API of the application.. Will open the default template and set the
        default values for this template. This class is dervived from the Page class """

    def show_page(self, **kwargs):
        # TODO: Implement and add DOCSTRING
        return 'API Page'
#---------------------------------------------------------------------------------------------------