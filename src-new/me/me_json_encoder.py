#!/usr/bin/env python3
"""
    me - me_json_encoder.py

    JSON encoder for the Me-application
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_database import Database
from json import JSONEncoder
#---------------------------------------------------------------------------------------------------
class MeJSONEncoder(JSONEncoder):
    """ JSON encoder for my own created classes """

    def default(self, obj):
        """ Gets the object and encodes it in a way JSON can work with """

        # Check if we can serialize this
        if isinstance(obj, Database.base_class):
            # If we receive a SQL Table class, we have to first get the columns;
            columns = [ column.name for column in type(obj).__table__.columns ]

            # Then we create a dict with the only the column items
            column_dict = { key: value for key, value in obj.__dict__.items() if key in columns }

            # And we return that dict
            return column_dict
        else:
            raise TypeError(
                "Unserializable object {} of type {}".format(obj, type(obj))
            )
#---------------------------------------------------------------------------------------------------