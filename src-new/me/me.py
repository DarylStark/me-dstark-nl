#!/usr/bin/env python3
"""
    me - me.py

    Contains the main class for the Me application. This class, called Me, can be used to run the
    complete application. The class is meant to be run as a static class; it is impossible to
    create instances of it.
"""
#---------------------------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------------------------
class Me:
    """ Main class for the Me application; creates all needed objects and does all needed tasks.
        This class is meant to run as a static class; it is impossible to create instances of it """

    # Class attributes. Will be filled as soon as the application is started
    # [...]

    def __new__(cls):
        """ When someone tries to create a instance of it, we give an error """
        raise Exception('It is impossible to create a instance of this class')
    
    @classmethod
    def start(cls):
        """ The start method start the actual application """
        pass
#---------------------------------------------------------------------------------------------------