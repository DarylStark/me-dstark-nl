#!/usr/bin/env python3
"""
    me - page_ui.py

    Class for the UI page of the application ('ui/*'). Will show the default UI template and adjust
    the variables in that
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import Page
#---------------------------------------------------------------------------------------------------
@Me.register_url(name = 'ui', regex = '^ui/?$')
class PageUI(Page):
    """ Class for the UI page of the application. Will show the default UI template and adjust the
        variables in that """

    def show_page(self, **kwargs):
        # TODO: Implement and add DOCSTRING
        return 'You are looking at the UI'
#---------------------------------------------------------------------------------------------------