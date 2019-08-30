#!/usr/bin/env python3
"""
    me - page_api_templates.py

    API module for '/api/templates'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import APIPage
from me import PageAPI
from me.exceptions import *
from template_loader import TemplateLoader, TemplateNotFoundException
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('templates')
class PageAPITemplates(APIPage):
    """ Class that can be called to run the API for templates """

    def __init__(self):
        """ The initiator for this object sets the API endpoints and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API endpoint gets in """
        
        self._api_endpoints = {
            'get': self.get
        }
    
    @PageAPI.api_endpoint(endpoint_name = 'get', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get(self, *args, **kwargs):
        """ API method to return a template from the TemploadLoader in the database """

        # Create a empty dict that will contain the templates to return later on
        return_templates = dict()

        # Get the templates the user wants
        try:
            templates = kwargs['templates'].split(',')
        except KeyError:
            raise MeAPITemplatesNoTemplatesGivenException('No templates given to retrieve')

        for template in templates:
            try:
                cnt = TemplateLoader.get_template(template, use_jinja = False)
                return_templates[template] = cnt
            except TemplateNotFoundException:
                raise MeAPITemplatesTemplateNotFoundException('Template "{template}" not found'.format(template = template))
        
        return ([ return_templates ], 1)
#---------------------------------------------------------------------------------------------------