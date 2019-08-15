#!/usr/bin/env python3
"""
    static_loader - static_loader.py

    Contains the main class for the StaticLoader
"""
#---------------------------------------------------------------------------------------------------
# Imports
from static_loader.exceptions import *
#---------------------------------------------------------------------------------------------------
class StaticLoader:
    """ Class to load a statis file and get it's contents. This is a static class, meaning that
        you can't create instances of it. Each static file that is loaded is placed in a cache for
        faster lookups in the feature. The item won't be placed in cache until it is requested and
        only when the application requests it to be placed in cache. This way, we can make sure that
        images, for instance, are not cached """
    
    # Class attributes
    static_directory = None
    _file_cache = {}

    def __new__(cls, *args, **kwargs):
        """ The __new__ method is called before __init__ and is repsponsible for creating the new
            instance of the class. When a user tries to create a instance of this class, we raise an
            error """
        raise TypeError('It is not possible to create instances of StaticLoader')
    
    @classmethod
    def load_file(cls, name):
        """ Method to (re-) load a file into the cache of the class. Will raise an error when
            something goes wrong, like a missing file """
        
        # Construct the correct filename
        filename = cls.static_directory + name

        # See if we can find an extension. If we can't, we have to raise an error cause it will be
        # impossible to find a mimetype for the file and it will be impossible to find if we have to
        # do a binary load
        fileparts = filename.split('.')
        print(fileparts)
        if len(fileparts) == 1:
            # TODO: Custom Exception
            raise ValueError('Extension for file "{}" couldn\'t be found'.format(file = name))
        
        # Get the extension
        extension = fileparts[-1].lower()

        # dict with known extensions, their loadtype and their mimetype
        extensions = {
            'png':  { 'binary': True,  'mimetype': 'image/png' },
            'jpg':  { 'binary': True,  'mimetype': 'image/jpeg' },
            'jpeg': { 'binary': True,  'mimetype': 'image/jpeg' },
            'gif':  { 'binary': True,  'mimetype': 'image/gif' },
            'js':   { 'binary': False, 'mimetype': 'text/javascript' },
            'css':  { 'binary': False, 'mimetype': 'text/css' }
        }

        # If we didn't register this extension, throw an error
        if not extension in extensions:
            # TODO: Custom Exception
            raise ValueError('Extension "{extension}" is not known'.format(extension = extension))
        
        # Get the correct mode to open the file
        mode = 'r'
        if extensions[extension]['binary']:
            mode = mode + 'b'
        
        # Open the file and get it's content
        try:
            with open(filename, mode) as static_file:
                # Get the file content
                cnt = static_file.readlines()

            # If this is a text file, we have to join the lines
            if not extensions[extension]['binary']:
                cnt = '\n'.join(cnt)    
        except FileNotFoundError:
            raise StaticFileNotFoundException('Static file "{name}" is not found'.format(name = name))
        else:
            # Set the loaded content in the cache
            cls._file_cache[name] = (cnt, extensions[extension]['mimetype'])
    
    @classmethod
    def get_file(cls, name, cache = True):
        """ Method to return a string with the contents of a file. The method will check if the
            file is already in cache and retrieves the template if it isn't. """

        # Check if static directory has a / at the end
        if cls.static_directory[-1] != '/': cls.static_directory += '/'
        
        # Check if we need to load the file
        if not name in cls._file_cache.keys():
            cls.load_file(name)
        
        # Get the contents from the cache and the mimetype to use
        contents, mimetype = cls._file_cache[name]

        # If we don't want to store this file in cache, remove it
        if not cache:
            del cls._file_cache[name]
        
        # Return the contents of the file from cache and the mimetype
        return (contents, mimetype)
#---------------------------------------------------------------------------------------------------