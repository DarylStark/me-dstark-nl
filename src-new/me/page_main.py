#!/usr/bin/env python3
"""
    me - page_main.py

    Class for the Main page of the application. Will open the default template and set the default
    values for this template.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import Page
from template_loader import TemplateLoader
#---------------------------------------------------------------------------------------------------
@Me.register_url(name = 'main', regex = '^$')
class PageMain(Page):
    """ Class for the Main page of the application. Will open the default template and set the
        default values for this template. This class is dervived from the Page class """

    def show_page(self, path, **kwargs):
        """ When the main page is openend, the user is presented with the option to log in. Since
            this application is a private application, we only show the Google Login button and
            nothing else """
        
        # Get the template for the loginpage
        loginpage = TemplateLoader.get_template('login')

        # Return the loginpage
        return loginpage
#---------------------------------------------------------------------------------------------------