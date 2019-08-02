#!/usr/bin/python3
"""
    Main entry point for the application. Supposed to be ran as script or by Google App Engine
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
#---------------------------------------------------------------------------------------------------
# Google App Engine uses the Flask object to serve the webpage. When developing, we use this file as
# a script. Therefore, when we start this application in the development environment, the __name__
# variable will be __main__. If it is, we can set the variables for the develop environment. All
# configuration comes from the same file, namely 'me-configuration.json' in the source-directory of
# the application. This file will be loaded in the Me-class after calling the method 'load_config'.
Me.load_config()

# We have loaded the config. We can now set the environment that we want to use. As stated before,
# we need to check the '__name__' variable to determine what environment to use.  We set the
# enviroment to 'development' now and overwrite it later on in the application.
Me.set_environment('development')

# We check if the '__name__' variable contains the string '__main__'. If it does, we are running
# this as a script and therefor on the development server.
if __name__ == '__main__':
    # Next, we can initiate the 'Me'-application. What this does, is creating a database connection
    # and making sure all needed tables exsist
    Me.initiate()

    # Start the application. We only need to do this on the development server; the Google App
    # Engine environment will start the application directly from the Flask-object in the Me class.
    Me.start()
else:
    # We are not running on the development server. Let's set the enviroment to 'production' so the
    # application can use the correct values.
    Me.set_environment('production')

    # Initiate the application
    Me.initiate()

    # Set the 'app' environment variable for Google App Engine
    app = Me.flask_app
#---------------------------------------------------------------------------------------------------