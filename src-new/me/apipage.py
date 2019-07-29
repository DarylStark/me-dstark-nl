#!/usr/bin/env python3
"""
    me - apipage.py

    Base class for API pages
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Page
from abc import abstractmethod
#---------------------------------------------------------------------------------------------------
class APIPage(Page):
    """ Base class for API pages. This class is abstract, meaning that it is impossible to create a
        instance of it """

    @abstractmethod
    def show_page(self, **kwargs):
        """ This method should exist in every class derived from this one. It gives the application
            a method to start when a instance of this class is started """
        pass
#---------------------------------------------------------------------------------------------------