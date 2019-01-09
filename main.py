#---------------------------------------------------------------------------------------------------
# main.py
#
# Date: 2018-12-20
#
# Main entry point for the application
#---------------------------------------------------------------------------------------------------
# Global imports
import os
import sys
import flask
import connexion
from flask import session
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

# Set the secret key for Flask-sessions
app.app.secret_key = '&\xf6\xd9\x97\x16Z\xa0\xdf\xf4\x8ak\xac0dDD\x0f\x7f\xf2\x1eV\x14-\x81'

# Add the API method to the Flask instance. We pass the configuration file that is defined in the
# 'flask_config" folder. This file can be used to create the complete API.
app.add_api(me_options['api_configfile'])

# A method to server static files
def serve_static(path, filename, mimetype, binary = False):
    """ Method to serve static content """
    try:
        # Set the flags for the open-context-manager
        flags = 'r'
        if binary:
            flags = 'rb'

        # Open the needed file
        with open('static/' + path + '/' + filename, flags) as f:
            cnt = f.readlines()

        # Generate the content
        if binary == False:
            cnt = ''.join(cnt)
        
        # Return the content
        return flask.Response(cnt, mimetype = mimetype)
    except:
        # Return a 404 error when something goes wrong
        flask.abort(404)

# Static folder for JavaScript files
@app.route('/js/<string:filename>', methods = [ 'GET'] )
def serve_javascript(filename):
    return serve_static('javascript', filename, 'application/javascript')

# Static folder for CSS files
@app.route('/css/<string:filename>', methods = [ 'GET'] )
def serve_css(filename):
    return serve_static('css', filename, 'text/css')

# Static folder for images
@app.route('/images/<string:filename>', methods = [ 'GET'] )
def serve_image(filename):
    return serve_static('images', filename, 'image/jpeg', binary = True)

@app.route('/login', methods = [ 'GET'] )
def login():
    if 'loggedin' in session:
        # User is already logged in. Redirect him to the homepage
        return flask.redirect('/', code = 302)
    else:
        # User is not logged in; show the loginpage
        # Create the object for the templates
        template = flask.render_template('login.html')
        return template

@app.route('/logout', methods = [ 'GET'] )
def logout():
    if 'loggedin' not in session:
        # User is not logged in. Redirect him to the loginpage
        return flask.redirect('/login', code = 302)
    else:
        # User is logged in. Show the default lougout page and destroy the session
        session.clear()
        template = flask.render_template('logout.html')
        return template

# Create a method that will be used when routed to '/'. This method opens the 'index.html' file in
# the directory with all the templates and returns it with the variables set.
@app.route('/', defaults = { 'path': '' }, methods = [ 'GET' ])
@app.route('/<path:path>', methods = [ 'GET' ])
def root_application(path):
    # Check if the user is logged in
    if 'loggedin' in session:
        # User menu (for logout and settings)
        user_menu = [
            { 'name': 'Settings' },
            { 'name': 'Logout' }
        ]

        # Main menu
        main_menu = {
            'menuitems': [
                { 'title': 'Feed', 'icon': 'view_stream', 'id': 'feed' },
                { 'title': 'Planning', 'icon': 'event', 'id': 'planning' }
            ],
            'submenus': [
                {
                    'name': 'Personal',
                    'subitems': [
                        { 'title': 'Concerts', 'icon': 'music_video', 'id': 'concerts' }
                    ]
                },
                { 'name': 'Professional' },
                { 'name': 'Study' }
            ]
        }

        # Variables for the template
        template_vars = {
            'pagetitle': 'Daryl Stark',
            'username': 'Daryl Stark',
            'user_menu': user_menu,
            'main_menu': main_menu
        }

        # Create the object for the templates
        template = flask.render_template('index.html', **template_vars)

        # Return the rendered version
        return template
    
    # User is not logged in. Redirect to the loginpage
    return flask.redirect('/login', code = 302)

# Check if we are running the file as a program, instead of a module
if __name__ == '__main__':
    # Start the Flask framework
    app.run(**me_options['flask'])
#---------------------------------------------------------------------------------------------------