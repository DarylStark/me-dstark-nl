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
    
    _registered_api_groups = {}

    def show_page(self, path, **kwargs):
        """ When 'show_page' for the API is called, we search through the registered API groups for
            the class to initate. As soon as we found it, we start it. If we can't find anything, we
            raise an Exception """
        
        # Get the group that the user requested
        splitted_path = path.split('/')
        if len(splitted_path) > 1:
            group = splitted_path[1].strip()
            if group != "":
                if group in type(self)._registered_api_groups.keys():
                    # Found the correct group. Let's create an instance of it
                    instance = type(self)._registered_api_groups[group]()

                    # Get the return value for it
                    return instance.show_page()
                else:
                    # TODO: Create custom Exception for this
                    raise NameError('API group "{group}" is not registered'.format(group = group))
            else:
                raise NameError('No API group specified')
        else:
            # No good API group given, raise an error
            # TODO: Create custom Exception for this
            raise NameError('No API group specified')
    
    @classmethod
    def register_api_group(cls, groupname):
        """ Decorator for classes to add classes to the stack of registered API groups """

        def decorator(class_):
            """ The decorator itself. Checks if the group already exists and register it if it
                doesn't """
            
            # First we check if the groupname is already registered
            if groupname in cls._registered_api_groups.keys():
                # TODO: Create custom Exception for this
                raise NameError('API group "{group}" is already registered'.format(group = groupname))
            else:
                # Then we register the group
                cls._registered_api_groups[groupname] = class_
            
            # We return the original class so it can still be used
            return class_
        
        # Return the decorator
        return decorator
#---------------------------------------------------------------------------------------------------