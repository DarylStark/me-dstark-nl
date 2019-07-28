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
    def show_page(self):
        # TODO: Create DOCSTRING
        pass
#---------------------------------------------------------------------------------------------------