#!/usr/bin/env python3
"""
    me - me_json_encoder.py

    JSON encoder for the Me-application
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_database import Database
from json import JSONEncoder
import datetime
#---------------------------------------------------------------------------------------------------
class MeJSONEncoder(JSONEncoder):
    """ JSON encoder for my own created classes """

    @staticmethod
    def convert_to_sa_dict(obj):
        """ Method to convert a SQLalchemy to a Python dict """
        # Get the columns
        columns = [ column.name for column in type(obj).__table__.columns ]

        # Then we create a dict with the only the column items
        column_dict = { key: value for key, value in obj.__dict__.items() if key in columns }

        # And we return that dict
        return column_dict

    def default(self, obj):
        """ Gets the object and encodes it in a way JSON can work with """

        # Serializer for database objects
        if isinstance(obj, Database.base_class):
            # Return the dict for the SQLalchemy object
            return MeJSONEncoder.convert_to_sa_dict(obj)
        # Serializer for datetime objects
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise TypeError(
                'Unserializable object "{}" of type "{}"'.format(obj, type(obj))
            )
#---------------------------------------------------------------------------------------------------