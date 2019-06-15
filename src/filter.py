#---------------------------------------------------------------------------------------------------
# filter.py
#
# Date: 2019-06-06
#
# Class to parse a filter
#---------------------------------------------------------------------------------------------------
# Global imports
import re
#---------------------------------------------------------------------------------------------------
class Filter:
    """ Class to parse filters

        A filter is build in fields. Each field starts with the fieldname, followed by a colon,
        followed by the text we need to filter for that specific field. If we need to filter on
        more than one word, we have to enclose the text in quotes.

        Example:

        archive:yes title:"Mandolin Orange"
    """

    def __init__(self, filter = None):
        """ Initiator sets the values for the object """
        self._filter = filter
        self._parsed = False
        self._parsed_filter = {}
    
    def parse(self):
        """ The method that does the actual parsing of the filter """
        # First, we need to find the fields that are set in this filter.
        filter_single = re.findall('([a-zA-Z0-9-]+):(\w+)', self._filter)
        filter_multiple = re.findall('([a-zA-Z0-9-]+):\"([^\"]+)\"', self._filter)
        allfields = filter_single + filter_multiple

        # Reset the parsed filter to default
        self._parsed_filter = {}

        # Create a dictionary with the fields
        for field in allfields:
            if field[0] in self._parsed_filter.keys():
                self._parsed_filter[field[0]] += [ field[1] ]
            else:
                self._parsed_filter[field[0]] = [ field[1] ]

        # Set _parsed to True so the rest of the object can check if the filter is parsed
        self._parsed = True
    
    @property
    def filter(self):
        """ Property for the filter """
        return self._filter
    
    @filter.setter
    def filter(self, filter):
        """ Setter for the filter property """
        self._filter = filter
        self._parsed = False
    
    @property
    def fields(self):
        """ Property for the fields. This will parse the filter if needed """
        if self._parsed == False:
            self.parse()
        
        return self._parsed_filter
#---------------------------------------------------------------------------------------------------