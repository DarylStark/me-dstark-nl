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
class MeAPIInvalidMethodException(MeException):
    """ Exception for when a API endpoints gets requested with the wrong HTTP method """
    pass
#---------------------------------------------------------------------------------------------------
class MeNoUserSessionException(MeException):
    """ Exception for when a user tries to open a protected page but a session doesn't exists """
    pass
#---------------------------------------------------------------------------------------------------
class MePermissionDeniedException(MeException):
    """ Exception for when a user with not permission tries to open a protected page """
    pass
#---------------------------------------------------------------------------------------------------
class MeAuthenticationFailedException(MeException):
    """ Exception for when a unauthenticated user tries to login """
    pass
#---------------------------------------------------------------------------------------------------
class MeNoLogoutKeyException(MeException):
    """ Exception for when a user tries to logout without a secret key """
    pass
#---------------------------------------------------------------------------------------------------
class MePageNotFoundException(MeException):
    """ Exception for when a user tries to open a page that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeNoFileProvidedException(MeException):
    """ Exception for when a user tries to open a static file directory """
    pass
#---------------------------------------------------------------------------------------------------
class MeSessionNotForUserException(MeException):
    """ Exception for when a user tries to update a UserSession name that isn't his """
    pass
#---------------------------------------------------------------------------------------------------
class MeActiveSessionCannotBeRemovedException(MeException):
    """ Exception for when a user tries to remove the currently active session """
    pass
#---------------------------------------------------------------------------------------------------
class MeUIConfigFileException(MeException):
    """ Exception for when the UI configuration file cannot be found or openend """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPITemplatesNoTemplatesGivenException(MeException):
    """ Exception for when the the user starts a template request without giving templates to
        retrieve """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPITemplatesTemplateNotFoundException(MeException):
    """ Exception for when the the user starts a template request for a template that doesn't
        exsist """
    pass
#---------------------------------------------------------------------------------------------------
class MeEMailAddressInvalidException(MeException):
    """ Exception for when the user tries to enter a invalid e-mail address """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINotesParentTagNotValidException(MeException):
    """ Exception for when a user specifies a parent tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINotesNoTagException(MeException):
    """ Exception for when a user tries to request a non-existing tag """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNotesTagNotValidException(MeException):
    """ Exception for when a user specifies a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------