#!/usr/bin/env python3
"""
    me - page_api_system.py

    API module for '/api/system'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import APIPage
from me import PageAPI
from me_database import Database
from static_loader import StaticLoader
from template_loader import TemplateLoader
from log import Log
from psutil import Process
import os
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('system')
class PageAPISystem(APIPage):
    """ Class that can be called to run the API for system """

    def __init__(self):
        """ The initiator for this object sets the API endpoints and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API endpoint gets in """
        
        self._api_endpoints = {
            'get_info': self.get_info,
        }

    @PageAPI.api_endpoint(endpoint_name = 'get_info', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_info(self, *args, **kwargs):
        """ Method to return system information """

        # Get the process ID (pid) and create a PSUtil Process object of it. We can use this later
        # to get specific information about the process
        pid = os.getpid()
        process = Process(pid)

        # Get information about the process
        process = {
            'pid': pid,
            'used_memory': process.memory_info().rss,
            'cpu_percentage': process.cpu_percent(),
            'username': process.username()
        }

        # Get information about the application
        # TODO: Make sure the TemplateLoader and StaticLoader cache sizes come from a method or
        # property instead of using the hidden variable '_*_cache'
        application = {
            'environment': Me.environment,
            'staticloader_files': len(StaticLoader._file_cache),
            'templateloader_files': len(TemplateLoader._template_cache)
        }

        # Get information about the database
        # TODO: Make a property in the Database class for this instead of using the hidden variable
        database = {
            'pool_size': Database._engine.pool.size(),
            'checked_in': Database._engine.pool.checkedin(),
            'overflow': Database._engine.pool.overflow(),
            'checked_out': Database._engine.pool.checkedout()
        }

        return([
            {
                'process': process,
                'application': application,
                'database': database
            }
        ], 0)
#---------------------------------------------------------------------------------------------------