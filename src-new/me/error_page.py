#!/usr/bin/env python3
"""
    me - error_page.py

    Module for a error-page class. Is used when a error occurs
"""
#---------------------------------------------------------------------------------------------------
# Imports
import me
from flask import Response
from template_loader import TemplateLoader


from static_loader import StaticLoader

import traceback
#---------------------------------------------------------------------------------------------------
class ErrorPage:
    """ Class to display errors in a nice way to the user. Static class; cannot be initiated """

    def __new__(cls, *args, **kwargs):
        """ The __new__ method is called before __init__ and is repsponsible for creating the new
            instance of the class. When a user tries to create a instance of this class, we raise an
            error """
        raise TypeError('It is not possible to create instances of ErrorPage')

    @classmethod
    def show_error(cls, error_code, error = None):
        """ Method to return a error page """

        # Find a error description that fits the error code
        error_descriptions = {
            403: 'You have no permission to the requested resource',
            404: 'The requested resource could not be found'
        }
        if error_code in error_descriptions.keys():
            error_description = error_descriptions[error_code]
        else:
            error_description = 'Unknown error'

        # Get the traceback object
        tb = traceback.format_exception(etype = type(error), value = error, tb = error.__traceback__)

        # Open the template for the error page
        tpl = TemplateLoader.get_template(
            'error',
            error_code = error_code,
            error_description = error_description,
            exception_name = error.__class__.__name__,
            exception_string = str(error),
            traceback = ''.join(tb),
            show_traceback = me.Me.get_configuration('errors', 'show_exceptions')
        )

        # TODO: Remove this!!!!!
        TemplateLoader._template_cache = dict()
        StaticLoader._file_cache = dict()

        # Create a response object
        return Response(tpl, error_code)
#---------------------------------------------------------------------------------------------------