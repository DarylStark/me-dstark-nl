#!/usr/bin/env python3
"""
    me - me.py

    Contains the main class for the Me application. This class, called Me, can be used to run the
    complete application. The class is meant to be run as a static class; it is impossible to
    create instances of it.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_database import Database
from me.exceptions import *
import flask
import re
import json
#---------------------------------------------------------------------------------------------------
class Me:
    """ Main class for the Me application; creates all needed objects and does all needed tasks.
        This class is meant to run as a static class; it is impossible to create instances of it """

    # Class attributes for Flask;
    # - The 'flask_app' is a class attribute that will be used as the main object for Flask. All
    #   Flask requests will be using this.
    # - The 'registered_urls' will be a dictionary. The keys are going to be regular expressions
    #   that can match a specific URL to a specific class. Within this class, a method will be
    #   mapped to every specific URL and will check if there is a matching regex. If there is, the
    #   class associated with the regex will be called to show the correct page. To register a class
    #   with a regex to this, the class should use the decorator Me.register_url.
    
    flask_app = flask.Flask(__name__)
    registered_urls = {}

    # Class attributes for Me;
    # - The 'configfile' is the file contains all the configuration for the application. It defaults
    #   to 'me-configuration.json', but can be changed by the calling script
    # - The 'config' will be the dict that contains the actual config.
    # - The 'environment' tells the class what environment we are in. The environment has to match a
    #   JSON key configuration file

    configfile = 'me-configuration.json'
    config = None
    environment = None

    def __new__(cls):
        """ When someone tries to create a instance of it, we give an error """
        raise Exception('It is impossible to create a instance of this class')
    
    @flask_app.route('/', defaults={'path': ''})
    @flask_app.route('/<path:path>')
    def show_page(path):
        """ Show the correct page based on registered regular expressions """

        # Search the registered_urls to see if there is any request that has a regex that matches
        # the given path. We do this for *all* registered URLs, even if we already found one to
        # see if there is a ambigious name. If there is, we have to throw an error
        matched_urls = [ (key, obj) for key, obj in Me.registered_urls.items() if obj['regex'].match(path) ]

        # Check how many results we have. If it is exactly one, we can continue. If it is zero, we
        # have to given the user a 404. If it is more then one, we have a ambigious name and we have
        # to give the user a error.
        if len(matched_urls) == 1:
            # Perfect match! Let's initiate a instance of the class that belongs to this registered
            # URL and start the 'show_page' method for that instance. We also have to give any
            # arguments that were given by the user (those things after the ? in the URL), if any.

            # Get the arguments that were given with the request
            args = dict(flask.request.values)

            # Initiate a instance of the registered class
            instance = matched_urls[0][1]['cls']()

            # Run the 'show_page' method and return the value of that method to Flask so it can show
            # the page
            return instance.show_page(path = path, **args)
        elif len(matched_urls) > 1:
            # Too many results; ambigious. Raise an error and tell the user which URLs are
            # conflicting. We tell the regexes that match as well.
            raise MeAmbigiousPathException('Ambigious path; matches regex of registered URLs: {urls}'.format(
                urls = ', '.join( [ '"{name}" ("{regex}")'.format(name = name, regex = obj['regex_text'] ) for name, obj in matched_urls ] )
            ))

        # No results; give a 404
        flask.abort(404)
    
    @classmethod
    def register_url(cls, regex, name):
        """ Decorator to register a URL to this static class. To register a URL, a class has to use
            this method as decorator. The decorator should be called with a regex that can match
            every URL that it should be used for and a unique name. This name isn't really used
            anywhere but can be very usefull in debugging """
        
        def decorator(class_):
            """ The real decorator method; will check if the regex is valid and register the class
                within this static class """
        
            # First, we check if the regex is valid. We do this trying to compile it. If it fails,
            # we know the regex is valid. AFAIK there is no other/better way of doing this
            try:
                compiled_regex = re.compile(regex)
            except re.error as Err:
                # Regex is not correct; raise an error
                raise MeRegexException(Err)
            else:
                # If the regex was valid, no error is raised. We need to check if this name is
                # unique. If it isn't; thrown an error
                if name in cls.registered_urls.keys():
                    raise MeAbigiousURLNameException('There is already a registered url with name "{name}"'.format(
                        name = name
                    ))

                # We can now register the URL. We
                # register URLs by their name. Within the dict for this key we register the given
                # compiled regular expression and the class that is given.
                cls.registered_urls[name] = {
                    'regex': compiled_regex,
                    'regex_text': regex,
                    'cls': class_
                }

                # After we register the class, we can return the class. If we don't do that, the
                # class will be unusable for other uses then this; it will simply stop existing in
                # the original form.
                return class_
            
            # Return the method
            return class_
        
        # Return the decorator
        return decorator
    
    @classmethod
    def load_config(cls):
        """ Load the configuration file """
        try:
            with open(cls.configfile, 'r') as cfgfile:
                cls.config = json.load(cfgfile)
        except FileNotFoundError:
            raise MeConfigFileException('File "{file}" doesn\'t exist'.format(file = cls.configfile))
        except json.decoder.JSONDecodeError:
            raise MeConfigFileException('File "{file}" is not valid JSON'.format(file = cls.configfile))
    
    @classmethod
    def set_environment(cls, environment):
        """ Set the environment of the configuration to use. Checks first if this environment is
            available in the configuration """
        
        # Check if the configuration is still None. If it is, load the configuration first
        if cls.config is None:
            cls.load_config()

        # Check if the asked environment exists and try to set it. If we get an AttributeError,
        # the configuration is still 'None'. We have to give the user a error in that specific
        # case.
        if environment in cls.config.keys():
            cls.environment = environment
        else:
            raise MeEnvironmentException('Environment "{environment}" does not exist'.format(environment = environment))
        
    @classmethod
    def get_configuration(cls, group, setting = None):
        """ Returns a configuration setting for a given group (like 'database') and a given setting
            (like 'database'). If 'setting' is not given, the complete dict for the group is
            returned """
        
        # Check if the given group exists
        if group in cls.config[cls.environment].keys():
            # If a setting is given ...
            if setting:
                # ... check if the settings exists
                if setting in cls.config[cls.environment][group].keys():
                    # Return the setting
                    return cls.config[cls.environment][group][setting]
                else:
                    # If the setting doesn't exist, raise an error
                    raise MeConfigException('Configuration group "{group}" does not contain a setting "{setting}"'.format(group = group, setting = setting))
            else:
                # If no setting is given, we return the complete dict for the group
                return cls.config[cls.environment][group]
        else:
            raise MeConfigException('Configuration group "{group}" does not exist'.format(group = group))
        
    @classmethod
    def initiate(cls):
        """ Method to do everything that needs to be done before the application can be started.
            This method will create the database connection and will make sure all tables in this
            database get created """
        
        # Check if the configuration is still None. If it is, load the configuration first
        if cls.config is None:
            cls.load_config()
        
        # Get the database configuration
        sql_settings = cls.get_configuration(group = 'database')
        
        # There are a few ways to connect to the MySQL server. The first way is connecting the
        # normal way using a TCP socket. The other way is with a Unix socket. This last method is
        # used by Google App Engine. When a instance is available in the configuration, we have to
        # use the Unix socket.
        if sql_settings['google_instance'] != '':
            connection_string = 'mysql+pymysql://{username}:{password}@/{database}?unix_socket=/cloudsql/{google_instance}'
        else:
            connection_string = 'mysql+pymysql://{username}:{password}@{server}/{database}'
        
        # Create a database connection. This will also add any tables that need to be added.
        Database.connect(connection_string.format(**sql_settings))
    
    @classmethod
    def start(cls):
        """ The start method start the actual application """

        # Start Flask with the configuration that is red in
        cls.flask_app.run(**cls.get_configuration('flask'))
#---------------------------------------------------------------------------------------------------