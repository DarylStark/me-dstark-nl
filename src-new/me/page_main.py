#!/usr/bin/env python3
"""
    me - page_main.py

    Class for the Main page of the application. Will open the default template and set the default
    values for this template.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import Page
#---------------------------------------------------------------------------------------------------
@Me.register_url(name = 'main', regex = '^$')
class PageMain(Page):
    """ Class for the Main page of the application. Will open the default template and set the
        default values for this template. This class is dervived from the Page class """

    def show_page(self, **kwargs):
        # TODO: Implement and add DOCSTRING
        return 'Main Page'
#---------------------------------------------------------------------------------------------------