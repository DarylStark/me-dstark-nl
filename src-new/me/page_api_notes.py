#!/usr/bin/env python3
"""
    me - page_api_notes.py

    API module for '/api/notes'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
from me import Me
from me.exceptions import *
from me_database import NoteTag, DatabaseSession
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('notes')
class PageAPINotes(APIPage):
    """ Class that can be called to run the API for notes """

    def __init__(self):
        """ The initiator for this object sets the API endpoints and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API endpoint gets in """
        
        self._api_endpoints = {
            'get_tags': self.get_tags
        }
    
    @PageAPI.api_endpoint(endpoint_name = 'get_tags', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_tags(self, *args, **kwargs):
        """ The 'get_tags' API endpoint returns tags for the notes. If no parent is given, it
            returns all tags that have no parent (and thus, are in the root). If a parent is given,
            it returns the tags for that parent """
        
        # Check if we got a parent
        parent = None
        if 'parent' in kwargs.keys():
            # Parent given
            parent = kwargs['parent']

            # Check if the parent is valid
            with DatabaseSession() as session:
                tags = session.query(NoteTag).filter(NoteTag.id == parent)
                if tags.count() != 1:
                    # TODO: Custom Error
                    raise MeAPINotesParentTagNotValidException('The tag {tag} is not a valid parent tag'.format(tag = parent))
        
        # Get the tags
        all_tags = list()
        with DatabaseSession() as session:
            # Get all users from the database
            tags = session.query(NoteTag).filter(NoteTag.parent == parent).order_by(NoteTag.name)
            
            # Get the usercount
            alltags = tags.count()

            # Get all the user objects
            all_tags = tags.all()
        
        return (all_tags, alltags)
#---------------------------------------------------------------------------------------------------