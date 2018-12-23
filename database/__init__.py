#---------------------------------------------------------------------------------------------------
# Package: database
# __init__.py
#
# Date: 2018-12-21
#
# Initiator for the 'database' package. Imports all the classes from the package.
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
import sqlalchemy.ext.declarative
#---------------------------------------------------------------------------------------------------
# We have to create a base class for the models that we are going to create and use
BaseClass = sqlalchemy.ext.declarative.declarative_base()
#---------------------------------------------------------------------------------------------------
from database.Database import Database
from database.Event import Event
#---------------------------------------------------------------------------------------------------