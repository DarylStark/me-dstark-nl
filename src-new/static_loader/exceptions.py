#!/usr/bin/env python3
"""
    static_loader - exceptions
    Author: Daryl Stark

    Module with custom exceptions for 'static_loader'
"""
#---------------------------------------------------------------------------------------------------
class StaticLoaderException(Exception):
    """ Base exception for Me exceptions """
    # TODO: Add this to the unittests
    pass
#---------------------------------------------------------------------------------------------------
class StaticFileNotFoundException(StaticLoaderException):
    """ Exception for when the user tries to open a static file that doesn't exist """
    # TODO: Add this to the unittests
    pass
#---------------------------------------------------------------------------------------------------