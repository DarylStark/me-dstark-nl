#!/usr/bin/env python3
"""
    me - exceptions
    Author: Daryl Stark

    Module with custom exceptions for 'me'
"""
#---------------------------------------------------------------------------------------------------
class MeException(Exception):
    """ Base exception for Me exceptions """
    pass
#---------------------------------------------------------------------------------------------------
class MeAmbigiousPathException(MeException):
    """ Exception for when the user tries to open a Flask page, but the Me-class find two ore more
        regexes that can be used for this page """
    pass
#---------------------------------------------------------------------------------------------------
class MeRegexException(MeException):
    """ Exception for when a regex is not compilable """
    pass
#---------------------------------------------------------------------------------------------------
class MeAbigiousURLNameException(MeException):
    """ Exception for when a regex is not compilable """
    pass
#---------------------------------------------------------------------------------------------------
class MeConfigFileException(MeException):
    """ Exception for when the configfile can't be found or is not valid JSON """
    pass
#---------------------------------------------------------------------------------------------------
class MeConfigException(MeException):
    """ Exception for a configuration item is requested that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeEnvironmentException(MeException):
    """ Exception for when a environment gets set that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGroupNotRegisteredException(MeException):
    """ Exception for when a API group gets requested that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINoAPIGroupException(MeException):
    """ Exception for when a no API group gets specified """
    pass
#---------------------------------------------------------------------------------------------------
class MeValueException(MeException):
    """ Exception for when a API value gets set to a wrong value """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIUnsupportedFormatException(MeException):
    """ Exception for when a API format gets requested that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIEndPointInvalidException(MeException):
    """ Exception for when a invalid API endcall get's called    """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINoEndPointException(MeException):
    """ Exception for when a no API endcall is specified """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIInvalidReturnException(MeException):
    """ Exception for when a API endpoints returns the wrong format """
    pass
#---------------------------------------------------------------------------------------------------