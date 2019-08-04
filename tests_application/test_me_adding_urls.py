#!/usr/bin/env python3
#---------------------------------------------------------------------------------------------------
# Import the pytest module for the testing
import pytest
#---------------------------------------------------------------------------------------------------
# Set the correct path to the 
import sys
sys.path.append("src-new/")
#---------------------------------------------------------------------------------------------------
from me import Me, Page
#---------------------------------------------------------------------------------------------------
class TestAddingURLs:
    """ Unit testing class to test if we can register URLs for the application """

    def test_adding_urls(self):
        """ Method to test if we can add URLs to the Me class """

        # Create a list of tuples with names and regexes to register
        urls = [
            ('test1', 'test1/.*'), ('test2', 'test2/.*'), ('test3', 'test3/.*'), ('test4', 'test4/.*')
        ]

        # Loop through the list and try to register each page
        for name, regex in urls:
            # Create a class and use the decorator for it
            @Me.register_url(name = name, regex = regex)
            class PageTest(Page):
                pass
            
            # Check if it is registered
            if name in Me.registered_urls.keys():
                # Check if the regex we set is correct
                if Me.registered_urls[name]['regex_text'] == regex:
                    assert True
                else:
                    assert False, 'The Me-class registered our test URL, but saved the wrong regex'
            else:
                assert False, 'The Me-class didn\'t register our test URL'
#---------------------------------------------------------------------------------------------------