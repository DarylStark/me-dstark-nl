#!/usr/bin/env python3
"""
    me - page.py

    Abstract main class for pages. Can and should be used as base class for pages. Sets the default
    values in the __init__ method and defines methods that should be used in any derived class.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from abc import ABC, abstractmethod
#---------------------------------------------------------------------------------------------------
class Page(ABC):
    """ Abstract base class for pages. Can and should be used as base class for pages """

    @abstractmethod
    def show_page(self, page, **kwargs):
        """ This method should exist in every class derived from this one. It gives the application
            a method to start when a instance of this class is started """
        pass
#---------------------------------------------------------------------------------------------------