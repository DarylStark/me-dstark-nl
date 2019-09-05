#!/usr/bin/env python3
"""
    me - page_api_notes.py

    API module for '/api/notes'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
from me import MeJSONEncoder
from me import Me
from me.exceptions import *
from me_database import NoteTag, DatabaseSession
from sqlalchemy import and_
import flask
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('notes')
class PageAPINotes(APIPage):
    """ Class that can be called to run the API for notes """

    def __init__(self):
        """ The initiator for this object sets the API endpoints and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API endpoint gets in """
        
        self._api_endpoints = {
            'get_tags': self.get_tags,
            'get_tag': self.get_tag,
            'add_tag': self.add_tag
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
            # Get all tag from the database
            tags = session.query(NoteTag).filter(NoteTag.parent == parent).order_by(NoteTag.name)
            
            # Get the tagcount
            alltags = tags.count()

            # Get all the tag objects
            all_tags = tags.all()
        
        return (all_tags, alltags)
    
    @PageAPI.api_endpoint(endpoint_name = 'get_tag', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_tag(self, *args, **kwargs):
        """ The 'get_tag' API endpoint returns detailed information for a specific tag """
        
        # Get the tag
        with DatabaseSession() as session:
            # Get all users from the database
            try:
                tag = session.query(NoteTag).filter(NoteTag.id == kwargs['tag'])
            except KeyError:
                # If the user didn't specify a tag, give an error
                raise MeAPINotesNoTagException('No tag given')
            else:
                # If we found too much tags, give an errors
                if tag.count() != 1:
                    raise MeAPINotesNoTagException('Tag {tag} couldn\'t be found'.format(tag = kwargs['tag']))
                
                # Found the tag. Let's see what the parent is
                tag = tag.first()
                parent = tag.parent

                # Create a dict from the tag
                tag = MeJSONEncoder.convert_to_sa_dict(tag)
                tag['parent_name'] = None

                # Find the parent (if there is one)
                if parent:
                    parent_tag = session.query(NoteTag).filter(NoteTag.id == parent)

                    if parent_tag.count() == 1:
                        # Add the parent name to the tag
                        parent_tag = parent_tag.first()
                        tag['parent_name'] = parent_tag.name
        
        return ([ tag ], 1)

    @PageAPI.api_endpoint(endpoint_name = 'add_tag', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def add_tag(self, *args, **kwargs):
        """ API endpoint to add tags """
        
        # Get the variables for the request
        parent_tag = flask.request.form.get('parent_tag')
        tag_name = flask.request.form.get('tag_name')

        # Flask treats variables it gets without a value as an empty string. SQLalchemy can't add
        # this, so we have to make it a None object when this happends
        if parent_tag == '':
            parent_tag = None

        # Start a session
        with DatabaseSession(commit_on_end = True) as session:
            # Check if a tag like this already exists
            tags = session.query(NoteTag).filter(
                and_(
                    NoteTag.parent == parent_tag,
                    NoteTag.name == tag_name
                )
            )

            # If the tag already exists, we give an error
            if tags.count() > 0:
                # TODO: Custom Error
                raise ValueError('A tag with the name "{name}" already exists within parent tag {tag}'.format(name = tag_name, tag = parent_tag))
            
            # Create a new NoteTag object with the new details
            new_entry = NoteTag(
                parent = parent_tag,
                name = tag_name
            )

            # Add the new entry
            session.add(new_entry)
        
        return ([ 'added' ], 1)
#---------------------------------------------------------------------------------------------------