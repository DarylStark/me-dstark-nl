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
from me.exceptions import *
from static_loader import *
from template_loader import TemplateLoader
from log import Log
import re
import flask
import json
#---------------------------------------------------------------------------------------------------
@Me.register_url(name = 'ui', regex = '^ui/?.?')
class PageUI(Page):
    """ Class for the UI page of the application. Will show the default UI template and adjust the
        variables in that. This class is also responsible for loading static files, like JavaScript
        files, images and CSS files. """

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
            '^ui/unprotected-js/.?': self.show_unprotected_js,
            '^ui/unprotected-img/.?': self.show_unprotected_image,
            '^ui/unprotected-css/.?': self.show_unprotected_css,
            '^ui/?.?': self.show_page_ui
        }
        
        # Find the page to display and display it
        for regex, method in pages.items():
            if re.match(regex, path):
                return method(path = path, **kwargs)
        
        # If we didn't return any, give an error
        raise MePageNotFoundException('Page "{path}" could not be found'.format(path = path))
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_page_ui(self, path, **kwargs):
        """ Method to show a the main page of the website """

        # Check if the UI configuration is already loaded and if it isn't, load it from the JSON
        # file
        if Me.config_ui is None:
            try:
                # Load the configfile into memeory
                Log.log(severity = Log.DEBUG, module = 'PageUI', message = 'Loading UI configuration into memory')
                with open(Me.configfile_ui, 'r') as ui_cfg:
                    Me.config_ui = json.load(ui_cfg)
            except FileNotFoundError:
                # File was not found; raise an error
                Log.log(severity = Log.ERROR, module = 'PageUI', message = 'Couldn\'t open ui-configuration file: "{file}"'.format(file = Me.configfile_ui))
                raise MeUIConfigFileException('Couldn\'t open ui-configuration file: "{file}"'.format(file = Me.configfile_ui))
            except json.decoder.JSONDecodeError:
                # File was not found but not valid JSON; raise an error
                Log.log(severity = Log.ERROR, module = 'PageUI', message = 'Couldn\'t open ui-configuration file: "{file}"'.format(file = Me.configfile_ui))
                raise MeUIConfigFileException('File "{file}" is not valid JSON'.format(file = Me.configfile_ui))
        
        # Load the 'ui.html' template and replace the needed variables
        template = TemplateLoader.get_template(
            'ui',
            **Me.config_ui['template_variables']['ui']
        )

        # TODO: Remove this debugging
        TemplateLoader._template_cache = dict()
        StaticLoader._file_cache = dict()
        Me.config_ui = None

        # Return the generated template
        return template   
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_protected_js(self, path, **kwargs):
        """ Method to show a protected JavaScript file """

        # Find the file to open
        static_file = re.findall('ui/js/([a-zA-Z0-9-\._]+)', path)
        if len(static_file) != 1:
            raise MeNoFileProvidedException

        # Open the file from the StaticLoader
        try:
            contents, mimetype = StaticLoader.get_file('protected-js/' + static_file[0])
        except StaticFileNotFoundException:
            raise MePageNotFoundException
        
        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_protected_image(self, path, **kwargs):
        """ Method to show a protected images. These images won't get cached in the application to
            spare memory """

        # Find the file to open
        static_file = re.findall('ui/img/([a-zA-Z0-9-\._]+)', path)
        if len(static_file) != 1:
            raise MeNoFileProvidedException

        # Open the file from the StaticLoader
        try:
            contents, mimetype = StaticLoader.get_file('protected-img/' + static_file[0], cache = False)
        except StaticFileNotFoundException:
            raise MePageNotFoundException

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.INTERACTIVE_USERS  })
    def show_protected_css(self, path, **kwargs):
        """ Method to show a protected CSS files """
        
        # Find the file to open
        static_file = re.findall('ui/css/([a-zA-Z0-9-\._]+)', path)
        if len(static_file) != 1:
            raise MeNoFileProvidedException

        # Open the file from the StaticLoader
        try:
            contents, mimetype = StaticLoader.get_file('protected-css/' + static_file[0])
        except StaticFileNotFoundException:
            raise MePageNotFoundException

        # Return it
        return flask.Response(contents, mimetype = mimetype)

    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_unprotected_js(self, path, **kwargs):
        """ Method to show a unprotected JavaScript files """
        
        # Find the file to open
        static_file = re.findall('ui/unprotected-js/([a-zA-Z0-9-\._]+)', path)
        if len(static_file) != 1:
            raise MeNoFileProvidedException

        # Open the file from the StaticLoader
        try:
            contents, mimetype = StaticLoader.get_file('unprotected-js/' + static_file[0])
        except StaticFileNotFoundException:
            raise MePageNotFoundException

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_unprotected_image(self, path, **kwargs):
        """ Method to show a unprotected images. These images won't get cached in the application to
            spare memory """

        # Find the file to open
        static_file = re.findall('ui/unprotected-img/([a-zA-Z0-9-\._]+)', path)
        if len(static_file) != 1:
            raise MeNoFileProvidedException

        # Open the file from the StaticLoader
        try:
            contents, mimetype = StaticLoader.get_file('unprotected-img/' + static_file[0], cache = False)
        except StaticFileNotFoundException:
            raise MePageNotFoundException

        # Return it
        return flask.Response(contents, mimetype = mimetype)
    
    @Me.ui_page(allowed = { Me.LOGGED_OFF  })
    def show_unprotected_css(self, path, **kwargs):
        """ Method to show a unprotected CSS files """
        
        # Find the file to open
        static_file = re.findall('ui/unprotected-css/([a-zA-Z0-9-\._]+)', path)
        if len(static_file) != 1:
            raise MeNoFileProvidedException

        # Open the file from the StaticLoader
        try:
            contents, mimetype = StaticLoader.get_file('unprotected-css/' + static_file[0])
        except StaticFileNotFoundException:
            raise MePageNotFoundException

        # Return it
        return flask.Response(contents, mimetype = mimetype)
#---------------------------------------------------------------------------------------------------