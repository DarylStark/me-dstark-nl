#---------------------------------------------------------------------------------------------------
# Venue.py
#
# Date: 2018-12-23
#
# Class for venues. A venue represents a organization that has its own stages for events, like
# TivoliVredenburg or Pandora.
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class Venue(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tVenues'

    # Set constrains for this table
    __table_args__ = (
        sqlalchemy.UniqueConstraint('Venue_Name'),
    )

    # Create the columns
    id = sqlalchemy.Column('Venue_ID', sqlalchemy.Integer, primary_key = True)
    name = sqlalchemy.Column('Venue_Name', sqlalchemy.VARCHAR(128), nullable = False)
#---------------------------------------------------------------------------------------------------