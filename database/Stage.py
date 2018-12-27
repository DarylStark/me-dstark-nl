#---------------------------------------------------------------------------------------------------
# Stage.py
#
# Date: 2018-12-23
#
# Class for stages. A stage represents a specific stage for events, like De Ronda in
# TivoliVredenburg or De Grote Zaal in Paradiso. Each stage has its own address.
#---------------------------------------------------------------------------------------------------
# Global imports
import sqlalchemy
#---------------------------------------------------------------------------------------------------
# Local imports
import database
#---------------------------------------------------------------------------------------------------
class Stage(database.BaseClass):
    # Set the tablename for this object
    __tablename__ = 'tStages'

    # Set constrains for this table
    __table_args__ = (
        sqlalchemy.UniqueConstraint('Stage_Venue', 'Stage_Name'),
    )

    # Create the columns
    id = sqlalchemy.Column('Stage_ID', sqlalchemy.Integer, primary_key = True)
    venue = sqlalchemy.Column('Stage_Venue', sqlalchemy.ForeignKey("tVenues.Venue_ID"), nullable = False)
    name = sqlalchemy.Column('Stage_Name', sqlalchemy.VARCHAR(128))
    address = sqlalchemy.Column('Stage_Address', sqlalchemy.Text)
    zipcode = sqlalchemy.Column('Stage_Zipcode', sqlalchemy.Text)
    city = sqlalchemy.Column('Stage_City', sqlalchemy.Text)
    country = sqlalchemy.Column('Stage_Country', sqlalchemy.Text)
#---------------------------------------------------------------------------------------------------