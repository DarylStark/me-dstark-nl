#!/usr/bin/env python3
"""
    template_loader - exceptions
    Author: Daryl Stark

    Module with custom exceptions for 'template_loader'
"""
#---------------------------------------------------------------------------------------------------
class TemplateLoaderException(Exception):
    """ Base exception for Me exceptions """
    pass
#---------------------------------------------------------------------------------------------------
class TemplateNotFoundException(TemplateLoaderException):
    """ Exception for when the user tries to open a template that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------