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

            # We create small lambda-functions to set default values for 'values'. The small lambda
            # methods will set a value for the 'values' to a default value if not set.
            default_int = lambda key, default: int(kwargs[key]) if key in kwargs.keys() else int(default)
            default_str = lambda key, default: str(kwargs[key]) if key in kwargs.keys() else str(default)

            # Set the default values for the the given variables. A variable is given using the URL.
            # It is done by setting '?variable=value' in the URL. For every variable we need to set,
            # we have a entry in the 'keys' list. Each entry is a tuple with three elements;
            # - The first is the function to use to set the default. The lambda methods above can be
            #   used for that
            # - The second element is the variable that we need to set the default for
            # - The thirs element is the default value
            keys = [ (default_int, 'limit', 25), (default_int, 'page', 1), (default_str, 'format', 'json') ]
            for default_value in keys:
                try:
                    kwargs[default_value[1]] = default_value[0](*default_value[1:])
                except ValueError:
                    # TODO: Create custom Exception for this
                    raise ValueError(
                        'Variable "{key}" should be "{default_type}". Got "{value_type}" with the value "{value}".'.format(
                            key = default_value[1],
                            default_type = type(default_value[2]).__name__,
                            value_type = type(kwargs[default_value[1]]).__name__,
                            value = kwargs[default_value[1]]
                        )
                    )
            
            # Run the given method for the API endpoint. We save the result in a variable so we can
            # put it in the resulting JSON later on.
            try:
                endpoint_result = method(self, *args, **kwargs)
            except:
                # TODO:
                # If the method raises an error, we should create a error-element to return to the
                # user. This element should contain enough information about the error so the user
                # can find out what to do.
                pass
            
            # Each API-endpoint should return a tuple. The tuple's first element will be the maximum
            # number of items in the set if a endless limit is given. The second item of the tuple
            # will be the returned data
            if not type(endpoint_result) is tuple:
                raise ValueError('Return value should be a tuple')

            # Create a dictionary to return later to the client
            return_dict = {
                'api_request': {
                    'path': path,
                    'group': self.group,
                    'values': kwargs
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

            # Get the runtime and set it in the returning object
            runtime = round(time() - start, 3)
            return_dict['api_response']['runtime'] = runtime

            # Check what kind of output we need. The default will be 'json'. The user can choose
            # between multiple options:
            # - json
            # - json_pretty
            if kwargs['format'] in [ 'json', 'json_pretty' ]:
                json_variables = {}
                if kwargs['format'] == 'json_pretty':
                    # Check if we need to format the JSON result in a nice format. If we do, we
                    # create a dict with the json.dumps parameters to set it to pretty. We can pass
                    # this dict later to the json.dumps method
                    json_variables = {
                        'indent': 4,
                        'sort_keys': True
                    }
                
                # Set the result for JSON
                result = json.dumps(return_dict, **json_variables)
                result_mimetype = 'application/json'
            else:
                # TODO: Create custom Exception for this
                raise ValueError('The format "{format}" is not supported'.format(format = kwargs['format']))
            
            # Return the new value
            return flask.Response(result, mimetype = result_mimetype)
        
        # Return the resulting method
        return decorator
#---------------------------------------------------------------------------------------------------