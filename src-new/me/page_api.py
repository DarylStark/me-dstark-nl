#!/usr/bin/env python3
"""
    me - page_aapi.py

    Class for the REST API of the application. Contains a decorator as well to modify API endpoints.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me.exceptions import *
from me import Page
from me import MeJSONEncoder
from time import time
from log import Log
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
                    raise MeAPIGroupNotRegisteredException('API group "{group}" is not registered'.format(group = group))
            else:
                raise MeAPINoAPIGroupException('No API group specified')
        else:
            # No good API group given, raise an error
            raise MeAPINoAPIGroupException('No API group specified')
    
    @classmethod
    def register_api_group(cls, groupname):
        """ Decorator for classes to add classes to the stack of registered API groups """

        def decorator(class_):
            """ The decorator itself. Checks if the group already exists and register it if it
                doesn't """
            
            # First we check if the groupname is already registered
            if groupname in cls._registered_api_groups.keys():
                raise MeAPIGroupAlreadyRegisteredException('API group "{group}" is already registered'.format(group = groupname))
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
    def api_endpoint(endpoint_name, allowed_methods = None, allowed_users = None):
        """ Decorator for API endpoints. Returns the API result at a consistent way. Each API
            endpoint using this decorator should return a tuple with the following values;
            - The first parameter is the data that is to be returned
            - The second element should be the maximum number of items in the table for the filter
              that is set. This allows the decorator to calculate the amount of possible pages.
        """

        def decorator(method):
            """ The decorator method is the real decorator """

            def endpoint(self, allowed_methods = allowed_methods, allowed_users = allowed_users, *args, **kwargs):
                """ Method that gets called for API endpoints with this decorator """

                # Check if the user allowed to run this method
                if not Me.check_allowed(allowed = allowed_users):
                    # TODO: Custom Exception
                    Log.log(severity = Log.NOTICE, module = 'API', message = 'Unauthorized user is trying to open API endpoint "{name}" in group "{group}".'.format(name = endpoint_name, group = self.group))
                    raise ValueError('Permission denied')

                # Get the starting time of the call so we can calculate the runtime afterwards
                start = time()

                # Check if this method (POST, GET, etc.) is allowed. The decorator gets called with
                # a named argument 'allowed_types'. The user can give a list of allowed methods for
                # this specific API. If the user doesn't give a list, we allow all methods
                request_method = flask.request.method.lower()
                if type(allowed_methods) != list:
                    # If no list is given for the allowed methods, we allow all
                    allowed_methods = [ 'get', 'post' ]
                
                # Check if the method is in the list. If it isn't, raise an error
                if not request_method in allowed_methods:
                    Log.log(severity = Log.NOTICE, module = 'API', message = 'User tried method "{method}" for endpoint "{name}" in group "{group}".'.format(method = request_method, name = endpoint_name, group = self.group))
                    raise MeAPIInvalidMethodException(
                        'Wrong HTTP method. Accepted methods are {methods}, got "{method}"'.format(
                            methods = ', '.join([ '"{x}"'.format(x = x) for x in allowed_methods ]),
                            method = request_method
                        )
                    )

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
                        Log.log(severity = Log.NOTICE, module = 'API', message = 'User gave wrong type for "{var}" in endpoint "{name}" in group "{group}".'.format(var = default_value[1], name = endpoint_name, group = self.group))
                        raise MeValueException(
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
                    raise MeAPIInvalidReturnException('Return value should be a tuple')

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
                        'data': endpoint_result[0],
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
                    result = json.dumps(return_dict, **json_variables, cls = MeJSONEncoder)
                    result_mimetype = 'application/json'
                else:
                    raise MeAPIUnsupportedFormatException('The format "{format}" is not supported'.format(format = kwargs['format']))
                
                # Return the new value
                return flask.Response(result, mimetype = result_mimetype)
            
            # Return the resulting method
            return endpoint
            
        # Return the decorator
        return decorator
#---------------------------------------------------------------------------------------------------