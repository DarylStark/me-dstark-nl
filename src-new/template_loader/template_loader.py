#!/usr/bin/env python3
"""
    template_loader - template_loader.py

    Contains the main class for the TemplateLoader
"""
#---------------------------------------------------------------------------------------------------
# Imports
from template_loader.exceptions import *
#---------------------------------------------------------------------------------------------------
class TemplateLoader:
    """ Class to load a template file and get it's contents. This is a static class, meaning that
        you can't create instances of it. Each template that is loaded is placed in a cache for
        faster lookups in the feature. The item won't be placed in cache until it is requested """
    
    # Class attributes
    template_directory = None
    template_extension = 'html'
    _template_cache = dict()

    def __new__(cls, *args, **kwargs):
        """ The __new__ method is called before __init__ and is repsponsible for creating the new
            instance of the class. When a user tries to create a instance of this class, we raise an
            error """
        raise TypeError('It is not possible to create instances of Database')
    
    @classmethod
    def load_template(cls, name):
        """ Method to (re-) load a template into the cache of the class. Will raise an error when
            something goes wrong, like a missing file """
        
        # Check if template directory has a / at the end
        if cls.template_directory[:1] != '/': cls.template_directory += '/'
        
        # Construct the correct filename
        filename = cls.template_directory + name + '.' + cls.template_extension
        
        # Open the file and get it's content
        try:
            with open(filename, 'r') as template:
                cnt = '\n'.join(template.readlines())
        except FileNotFoundError:
            raise TemplateNotFoundException('Template "{name}" is not found'.format(name = name))
        else:
            # Set the loaded content in the cache
            cls._template_cache[name] = cnt
    
    @classmethod
    def get_template(cls, name):
        """ Method to return a string with the contents of a template. The method will check if the
            template is already in cache and retrieves the template if it isn't. """
        
        # Check if we need to load the template
        if not name in cls._template_cache.keys():
            cls.load_template(name)
        
        # Return the contents of the template file from cache
        return cls._template_cache[name]
#---------------------------------------------------------------------------------------------------