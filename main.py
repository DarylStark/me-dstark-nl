#---------------------------------------------------------------------------------------------------
# main.py
#
# Date: 2018-12-20
#
# Main entry point for the application
#---------------------------------------------------------------------------------------------------
# Global imports
import os
import flask
import connexion
#---------------------------------------------------------------------------------------------------
me_options = {
    'configdir': 'flask_config/',
    'api_configfile': 'config_api.yaml',
    'flask': {
        'host': '127.0.0.1',
        'port': 8080,
        'debug': True
    }
}
#---------------------------------------------------------------------------------------------------
# Check if we are on Google App Engine. If we are, set some options differently
if 'gunicorn' in os.getenv('SERVER_SOFTWARE', ''):
    me_options['flask']['debug'] = False

# Create an instance of Flask. We use the 'connextion' module so we can easily create an documented,
# testable and configurable API
app = connexion.FlaskApp(
    __name__,
    specification_dir = me_options['configdir']
)

# Add the API method to the Flask instance. We pass the configuration file that is defined in the
# 'flask_config" folder. This file can be used to create the complete API.
app.add_api(me_options['api_configfile'])

# Create a method that will be used when routed to '/'
# TODO: make sure this is used for everything, except '/api/'
@app.route('/', methods = [ 'GET' ])
def root_application():
    return '<b>Insert homepage here</b>.'

# Check if we are running the file as a program, instead of a module
if __name__ == '__main__':
    # Start the Flask framework
    app.run(**me_options['flask'])
#---------------------------------------------------------------------------------------------------