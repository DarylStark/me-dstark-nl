#!/usr/bin/env python3
""" Unit testing class to test the TemplateLoader. Loads a template and checks if it is in the
    TemplateLoader cache
"""
#---------------------------------------------------------------------------------------------------
# Import the pytest module for the testing
import pytest
#---------------------------------------------------------------------------------------------------
# Set the correct path to the 
import sys
sys.path.append('src-new/')
#---------------------------------------------------------------------------------------------------
from template_loader import *
#---------------------------------------------------------------------------------------------------
class TestAddingURLs:
    """ Unit testing class to test if we load templates and if they stay in the cache """

    def test_loading_templates(self):
        """ Test to load a template and check the returned value """

        # Expected template contents
        expected = 'This is a test-template for the unit test test_templateloader. Do not change this file!'

        # Configure the TemplateLoader
        TemplateLoader.template_directory = 'tests_application/templates'
        
        # Load a template
        tpl = TemplateLoader.get_template('test-template')

        # Check if the given value is correct
        assert tpl == expected
    
    def test_replace_variables(self):
        """ Test to load a template, change a variable and check the returned value """

        # Expected template contents
        expected = 'This is a test-template for the unit test test_templateloader. Do not change this file! testvariable'

        # Configure the TemplateLoader
        TemplateLoader.template_directory = 'tests_application/templates'
        
        # Load a template
        tpl = TemplateLoader.get_template('test-template', testvariable = ' testvariable')

        # Check if the given value is correct
        assert tpl == expected

    def test_change(self):
        """ Test to load a template and check the returned value """

        # Expected template contents
        expected = 'This is a test-template for the unit test test_templateloader. Do not change this file!{{ testvariable }}'

        # Configure the TemplateLoader
        TemplateLoader.template_directory = 'tests_application/templates'
        
        # Load a template
        tpl = TemplateLoader.get_template('test-template')

        # Check if the given value is correct
        assert TemplateLoader._template_cache['test-template'] == expected
#---------------------------------------------------------------------------------------------------