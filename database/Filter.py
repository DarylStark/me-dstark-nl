#---------------------------------------------------------------------------------------------------
# Filter.py
#
# Date: 2019-01-18
#
# Class for filters. A filter can be used on a datapage
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class Filter(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tFilters'

    # Create the columns
    id = sqlalchemy.Column('Filter_ID', sqlalchemy.Integer, primary_key = True)
    page = sqlalchemy.Column('Filter_Page', sqlalchemy.Text, nullable = False)
    name = sqlalchemy.Column('Filter_Name', sqlalchemy.Text, nullable = False)
    filter = sqlalchemy.Column('Filter_Filter', sqlalchemy.Text, nullable = False)

    def get_dict(self):
        """ Method to represent the object as a dict """

        return {
            'id': self.id,
            'name': self.name,
            'page': self.page,
            'filter': self.filter
        }
#---------------------------------------------------------------------------------------------------