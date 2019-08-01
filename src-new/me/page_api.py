#!/usr/bin/env python3
"""
    me - page_aapi.py

    Class for the REST API of the application. Contains a decorator as well to modify API endpoints.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import Page
from time import time
import flask
import json
import math
import re
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
        group = re.findall('^[^/]+/(.+)/', path)
        if len(group) == 1:
            group = group[0]
            if group != "":
                if group in type(self)._registered_api_groups.keys():
                    # Found the correct group. Let's create an instance of it
                    instance = type(self)._registered_api_groups[group]()

                    # Get the return value for it
                    return instance.show_page(path, **kwargs)
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
                # Add a variable to the class with the name of the group. The class can use this to
                # display errors, for instance
                class_.group = groupname

                # Then we register the group
                cls._registered_api_groups[groupname] = class_
            
            # We return the original class so it can still be used
            return class_
        
        # Return the decorator
        return decorator
    
    @staticmethod
    def api_endpoint(method):
        """ Decorator for API endpoints. Returns the API result at a consistent way. Each API
            endpoint using this decorator should return a tuple with the following values;
            - The first parameter is the data that is to be returned
            - The second element should be the maximum number of items in the table for the filter
              that is set. This allows the decorator to calculate the amount of possible pages.
         """

        def decorator(self, *args, **kwargs):
            """ Method that gets called for API endpoints with this decorator """

            # Get the starting time of the call so we can calculate the runtime afterwards
            start = time()

            # Get the given arguments
            args = dict(flask.request.values)

            # Get the path (if given)
            path = None
            if 'path' in kwargs.keys():
                path = kwargs['path']

            # Set the limit
            try:
                kwargs['limit'] = int(kwargs['limit']) if 'limit' in kwargs.keys() else 25
            except ValueError:
                # TODO: Create custom Exception for this
                raise ValueError('Variable "limit" should be an number')
            
            # Set the pas
            try:
                kwargs['page'] = int(kwargs['page']) if 'page' in kwargs.keys() else 1
            except ValueError:
                # TODO: Create custom Exception for this
                raise ValueError('Variable "limit" should be an number')
            
            # Run the given method
            endpoint_result = method(self, *args, **kwargs)
            if not type(endpoint_result) is tuple:
                raise ValueError('Return value should be a tuple')

            # Create a dictionary to return
            return_dict = {
                'api_request': {
                    'path': path,
                    'group': self.group,
                    'values': args
                },
                'api_response': {
                    'runtime': None
                },
                'result': {
                    'data': endpoint_result,
                    'data_len': len(endpoint_result[0]),
                    'max_data_len': endpoint_result[1],
                    'limit': kwargs['limit'],
                    'max_page': math.ceil(endpoint_result[1] / kwargs['limit']),
                    'page': kwargs['page']
                }
            }

            # Check if we need to format the JSON result in a need format
            json_variables = {}
            if 'pretty' in kwargs:
                json_variables = {
                    'indent': 4,
                    'sort_keys': True
                }

            # Get the runtime and set it in the returning object
            runtime = round(time() - start, 3)
            return_dict['api_response']['runtime'] = runtime
            
            # Return the new value
            return flask.Response(json.dumps(return_dict, **json_variables), mimetype = 'application/json')
        
        # Return the resulting method
        return decorator
#---------------------------------------------------------------------------------------------------