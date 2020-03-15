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
class MeExceptionPermissionDeniedException(MeException):
    """ Base exception for 403-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeExceptionPageNotFoundException(MeException):
    """ Base exception for 404-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeExceptionServerErrorException(MeException):
    """ Base exception for 500-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeAmbigiousPathException(MeExceptionPageNotFoundException):
    """ Exception for when the user tries to open a Flask page, but the Me-class find two ore more
        regexes that can be used for this page """
    pass
#---------------------------------------------------------------------------------------------------
class MeRegexException(MeExceptionServerErrorException):
    """ Exception for when a regex is not compilable """
    pass
#---------------------------------------------------------------------------------------------------
class MeAbigiousURLNameException(MeExceptionServerErrorException):
    """ Exception for when a regex is not compilable """
    pass
#---------------------------------------------------------------------------------------------------
class MeConfigFileException(MeExceptionServerErrorException):
    """ Exception for when the configfile can't be found or is not valid JSON """
    pass
#---------------------------------------------------------------------------------------------------
class MeConfigException(MeExceptionServerErrorException):
    """ Exception for a configuration item is requested that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeEnvironmentException(MeExceptionServerErrorException):
    """ Exception for when a environment gets set that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGroupNotRegisteredException(MeExceptionPageNotFoundException):
    """ Exception for when a API group gets requested that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINoAPIGroupException(MeExceptionPageNotFoundException):
    """ Exception for when a no API group gets specified """
    pass
#---------------------------------------------------------------------------------------------------
class MeValueException(MeExceptionPageNotFoundException):
    """ Exception for when a API value gets set to a wrong value """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIUnsupportedFormatException(MeException):
    """ Exception for when a API format gets requested that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIEndPointInvalidException(MeExceptionPageNotFoundException):
    """ Exception for when a invalid API endcall get's called    """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINoEndPointException(MeExceptionPageNotFoundException):
    """ Exception for when a no API endcall is specified """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIInvalidReturnException(MeExceptionServerErrorException):
    """ Exception for when a API endpoints returns the wrong format """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIInvalidMethodException(MeExceptionPermissionDeniedException):
    """ Exception for when a API endpoints gets requested with the wrong HTTP method """
    pass
#---------------------------------------------------------------------------------------------------
class MeNoUserSessionException(MeExceptionPermissionDeniedException):
    """ Exception for when a user tries to open a protected page but a session doesn't exists """
    pass
#---------------------------------------------------------------------------------------------------
class MePermissionDeniedException(MeExceptionPermissionDeniedException):
    """ Exception for when a user with not permission tries to open a protected page """
    pass
#---------------------------------------------------------------------------------------------------
class MeAuthenticationFailedException(MeExceptionPermissionDeniedException):
    """ Exception for when a unauthenticated user tries to login """
    pass
#---------------------------------------------------------------------------------------------------
class MeNoLogoutKeyException(MeExceptionPermissionDeniedException):
    """ Exception for when a user tries to logout without a secret key """
    pass
#---------------------------------------------------------------------------------------------------
class MePageNotFoundException(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to open a page that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeNoFileProvidedException(MeExceptionPermissionDeniedException):
    """ Exception for when a user tries to open a static file directory """
    pass
#---------------------------------------------------------------------------------------------------
class MeSessionNotForUserException(MeExceptionPermissionDeniedException):
    """ Exception for when a user tries to update a UserSession name that isn't his """
    pass
#---------------------------------------------------------------------------------------------------
class MeActiveSessionCannotBeRemovedException(MeExceptionPermissionDeniedException):
    """ Exception for when a user tries to remove the currently active session """
    pass
#---------------------------------------------------------------------------------------------------
class MeUIConfigFileException(MeExceptionServerErrorException):
    """ Exception for when the UI configuration file cannot be found or openend """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPITemplatesNoTemplatesGivenException(MeExceptionPermissionDeniedException):
    """ Exception for when the the user starts a template request without giving templates to
        retrieve """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPITemplatesTemplateNotFoundException(MeExceptionPageNotFoundException):
    """ Exception for when the the user starts a template request for a template that doesn't
        exsist """
    pass
#---------------------------------------------------------------------------------------------------
class MeEMailAddressInvalidException(MeExceptionPermissionDeniedException):
    """ Exception for when the user tries to enter a invalid e-mail address """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINotesParentTagNotValidException(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a parent tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPINotesNoTagException(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to request a non-existing tag """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNotesTagNotValidException(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIAddNotesTagDuplicateNameException(MeExceptionPermissionDeniedException):
    """ Exception for when a user adds a tag that already exists """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIDeleteNotesTagInvalidTagException(MeExceptionPermissionDeniedException):
    """ Exception for when a user tries to delete a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIRenameNotesTagInvalidTagExceptionalueException(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNoteNoNoteExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNoteNoRevisionsExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to get a note with no revisions """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNoteInvalidNoteExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNoteInvalidRevisionExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNoteRevisionsNoNoteExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user doesn't specifiy a not when requesting revisions """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIGetNoteRevisionsNonExistingNoteExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user specifies a non-existing note when requesting revisions """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIEditNonExistingNoteExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to edit a note that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIAddNoteInvalidTagExeption(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to add a note with a tag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIDeleteNoteInvalidNoteException(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to delete a note that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeAPIDeleteNoteTagInvalidNoteException(MeExceptionPageNotFoundException):
    """ Exception for when a user tries to delete a NotesTag that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------