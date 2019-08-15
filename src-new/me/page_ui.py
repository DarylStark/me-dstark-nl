#!/usr/bin/env python3
"""
    me - page_ui.py

    Class for the UI page of the application ('ui/*'). Will show the default UI template and adjust
    the variables in that
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import Page
from static_loader import StaticLoader
import re
import flask
#---------------------------------------------------------------------------------------------------
@Me.register_url(name = 'ui', regex = '^ui/?.?')
class PageUI(Page):
    """ Class for the UI page of the application. Will show the default UI template and adjust the
        variables in that. This class is also responsible for loading static files, like JavaScript
        files, images and CSS files. """
    
    # TODO: Add this to the unittests

    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_page(self, path, **kwargs):
        """ Method to searches the path for what the user is trying to find and display the correct
            file. Can be either a (protected) static file like a image, JavaScript or CSS file or
            can be the main UI. """
        
        # We create a dict with the pages to display. Each key will be a regex that can match a
        # path. The value will be the method to run at that specific moment.
        pages = {
            '^ui/js/.?': self.show_protected_js,
            '^ui/img/.?': self.show_protected_image,
            '^ui/css/.?': self.show_protected_css,
            '^ui/login-js/.?': self.show_unprotected_js,
            '^ui/login-img/.?': self.show_unprotected_image,
            '^ui/login-css/.?': self.show_unprotected_css,
            '^ui/?.?': self.show_page_ui
        }
        
        # Find the page to display and display it
        for regex, method in pages.items():
            if re.match(regex, path):
                return method(path = path, **kwargs)
        
        # If we didn't return any, give an error
        # TODO: Custom exception
        raise ValueError
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_page_ui(self, path, **kwargs):
        """ Method to show a the main page of the website """
        return 'Main page'
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_protected_js(self, path, **kwargs):
        """ Method to show a protected JavaScript file """

        # Find the file to open
        static_file = re.findall('ui/js/([a-zA-Z0-9-\.]+)', path)
        if len(static_file) != 1:
            raise ValueError

        # Open the file from the StaticLoader
        contents, mimetype = StaticLoader.get_file('protected-js/' + static_file[0])

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_protected_image(self, path, **kwargs):
        """ Method to show a protected images. These images won't get cached in the application to
            spare memory """

        # Find the file to open
        static_file = re.findall('ui/img/([a-zA-Z0-9-\.]+)', path)
        if len(static_file) != 1:
            raise ValueError

        # Open the file from the StaticLoader
        contents, mimetype = StaticLoader.get_file('protected-img/' + static_file[0], cache = False)

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_protected_css(self, path, **kwargs):
        """ Method to show a protected CSS files """
        
        # Find the file to open
        static_file = re.findall('ui/css/([a-zA-Z0-9-\.]+)', path)
        if len(static_file) != 1:
            raise ValueError

        # Open the file from the StaticLoader
        contents, mimetype = StaticLoader.get_file('protected-css/' + static_file[0])

        # Return it
        return flask.Response(contents, mimetype = mimetype)

    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_unprotected_js(self, path, **kwargs):
        """ Method to show a unprotected JavaScript files """
        
        # Find the file to open
        static_file = re.findall('ui/login-js/([a-zA-Z0-9-\.]+)', path)
        if len(static_file) != 1:
            raise ValueError

        # Open the file from the StaticLoader
        contents, mimetype = StaticLoader.get_file('unprotected-js/' + static_file[0])

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_unprotected_image(self, path, **kwargs):
        """ Method to show a unprotected images. These images won't get cached in the application to
            spare memory """

        # Find the file to open
        static_file = re.findall('ui/login-img/([a-zA-Z0-9-\.]+)', path)
        if len(static_file) != 1:
            raise ValueError

        # Open the file from the StaticLoader
        contents, mimetype = StaticLoader.get_file('unprotected-img/' + static_file[0], cache = False)

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_unprotected_css(self, path, **kwargs):
        """ Method to show a unprotected CSS files """
        
        # Find the file to open
        static_file = re.findall('ui/login-css/([a-zA-Z0-9-\.]+)', path)
        if len(static_file) != 1:
            raise ValueError

        # Open the file from the StaticLoader
        contents, mimetype = StaticLoader.get_file('unprotected-css/' + static_file[0])

        # Return it
        return flask.Response(contents, mimetype = mimetype)
#---------------------------------------------------------------------------------------------------