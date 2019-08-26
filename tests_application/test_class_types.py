#!/usr/bin/env python3
""" Unit testing class to test the types of classes in the application. There are a few types of
    classes:
    - Classes can be normal
    - Some classed need to be a singleton, meaning only one instance of the class can exist)
    - Some classes need to be static, meaning no instances of it exists
    - Some classes are abstract, meaning they can only be used as base class
    - Some classes are exception classes, meaning they can be used as Exceptions
    This Test Class tests if all the classes are from the correct type
"""
#---------------------------------------------------------------------------------------------------
# Import the pytest module for the testing
import pytest
#---------------------------------------------------------------------------------------------------
# Set the correct path to the 
import sys
sys.path.append('src-new/')
#---------------------------------------------------------------------------------------------------
from me import *
from me_database import *
from template_loader import *
from static_loader import *
from log import *
#---------------------------------------------------------------------------------------------------
def classes(classes):
    """ Decorator for the test methods. Accepts the classes to be tested """

    def decorator(method):
        """ Decorator for the test methods. Raises the AssertionError when the method returns errors """
        
        def inner(self):
            """ The real decorator class. Runs the test and gets errors in return. If there are errors,
                we 'assert False' with the errors """

            # Run the method
            errors = method(self, classes = classes)

            # Check if we have errors. If we have, raise and False assertion so the check fails.
            # Otherwise, raise an True assertion for a succesfull test
            if len(errors) == 0:
                assert True
            else:
                # Create an string with the errors
                error_string = ', '.join([ 'Class "{class_}": "{error}"'.format(class_ = class_, error = error) for class_, error in errors.items() ])
                assert False, error_string

        return inner
    return decorator
#---------------------------------------------------------------------------------------------------
class TestClassTypes:
    """ Unit testing class to test the types of classes in the application. There are a few types of
        classes:
        - Classes can be normal
        - Some classed need to be a singleton, meaning only one instance of the class can exist)
        - Some classes need to be static, meaning no instances of it exists
        - Some classes are abstract, meaning they can only be used as base class
        - Some classes are exception classes, meaning they can be used as Exceptions
        This Test Class tests if all the classes are from the correct type """
    
    @classes(classes = [ PageAPIAAA, PageAPIEvents, PageAPIFeed, PageAPIUsers,
                         PageAPI, PageMain, PageUI, EventChange,
                         EventSyncResult, Event, FeedItemEventChange, FeedItem,
                         Filter, Stage, User, Venue,
                         UserSession, DatabaseSession ])
    def test_normal_classes(self, classes):
        """ Method to test all normal classes """

        # Empty list of errourness classes
        errors = {}
        
        # Loop through the classes and test if it is possible to create an instance from it, a
        # second instance and if they are different from eachother
        for class_ in classes:
            try:
                # Create two instances of the class to check if it is possible to create instances
                # of it
                obj1 = class_()
                obj2 = class_()

                # Check if they are the same object. If they are the same, they are not correct so
                # we throw an error
                if obj1 is obj2:
                    raise Exception('Instances of class "{name}" "obj1" and "obj2" are the same object ({id})'.format(
                        name = class_.__name__,
                        id = id(obj1)
                    ))
            except Exception as err_message:
                errors[class_.__name__] = err_message
        
        # Return the errors to the decorator
        return errors
    
    @classes(classes = [ Me, Database, TemplateLoader, Log ])
    def test_static_classes(self, classes):
        """ Method to test static classes """

        # Empty list of errourness classes
        errors = {}

        # Loop through the classes and test if it is possible to create an instance from it. If it
        # is, the test should fail
        for class_ in classes:
            try:
                obj1 = class_()
            except Exception as err_message:
                # If we receive an error, the class is correct
                pass
            else:
                errors[class_.__name__] = 'Could create an instance of this static class'
        
        # Return the errors to the decorator
        return errors
    
    @classes(classes = [ APIPage, Page ])
    def test_abstract_classes(self, classes):
        """ Method to test static classes """
        
        # Empty list of errourness classes
        errors = {}

        # Loop through the classes and test if it is possible to create an instance from it. If it
        # is, the test should fail
        for class_ in classes:
            try:
                obj1 = class_()
            except Exception as err_message:
                # If we receive an error, the class is correct
                pass
            else:
                errors[class_.__name__] = 'Could create an instance of this abstract class'
        
        # Return the errors to the decorator
        return errors
    
    @classes(classes = [ MeException, MeAmbigiousPathException, MeRegexException, MeAbigiousURLNameException,
                         MeConfigFileException, MeConfigException, MeEnvironmentException, MeAPIGroupNotRegisteredException,
                         MeAPINoAPIGroupException, MeValueException, MeAPIUnsupportedFormatException, MeAPIEndPointInvalidException,
                         MeAPINoEndPointException, MeAPIInvalidReturnException, TemplateLoaderException, TemplateNotFoundException,
                         MeAPIInvalidMethodException, StaticLoaderException, StaticFileNotFoundException, MeNoUserSessionException,
                         MePermissionDeniedException, MeAuthenticationFailedException, MeNoLogoutKeyException, MePageNotFoundException,
                         MePageNotFoundException, MeNoFileProvidedException, MeSessionNotForUserException, MeActiveSessionCannotBeRemovedException,
                         MeUIConfigFileException ])
    def test_exception_classes(self, classes):
        """ Method to test if a class is a exception class """

        # Empty list of errourness classes
        errors = {}

        # Loop through the classes and test if it is possible to create an instance from it. If it
        # is, the test should fail
        for class_ in classes:
            try:
                if not isinstance(class_(), Exception):
                    raise Exception('Not an exception class')
            except Exception as err_message:
                errors[class_.__name__] = err_message
        
        # Return the errors to the decorator
        return errors
#---------------------------------------------------------------------------------------------------