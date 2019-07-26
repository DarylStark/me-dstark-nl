#!/usr/bin/python3
"""
    Main entry point for the application. Supposed to be ran as script or by Google App Engine
"""
#---------------------------------------------------------------------------------------------------
# Imports
import flask
#---------------------------------------------------------------------------------------------------
class Me:
    """ Main class for the Me application; creates all needed objects and does all needed tasks.
        This class will be a Singleton; only one instance of it can be created. This way, I can make
        sure needed resources are limited """
    
    # Class attributes
    _singleton_instance = None

    def __new__(cls):
        """ The '__new__' method gets called when a instance of the class gets created. By making
            sure a existing instance will always be returned when creating a new instance, we can
            make sure only one instance for the application exists """
        
        # We create a singleton by checking if there is already a instance of a object. If there is,
        # we return the already existing instance. If there isn't, we create a new one and return
        # that.
        if cls._singleton_instance is None:
            cls._singleton_instance = super(Me, cls).__new__(cls)
        return cls._singleton_instance
    
    def __init__(self):
        """ The init method sets some default variables for the instance """
        pass
    
    def start(self):
        """ The start method start the actual application """
        pass
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Create a instance of the Me class. This will be the main application
    me = Me()
    me.start()
#---------------------------------------------------------------------------------------------------