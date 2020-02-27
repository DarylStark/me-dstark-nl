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
from me_database import NoteTag, NotesTags, DatabaseSession, Note, NoteRevision
from sqlalchemy import and_, desc
from sqlalchemy.orm import load_only
import flask
import markdown
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
            'add_tag': self.add_tag,
            'delete_tag': self.delete_tag,
            'rename_tag': self.rename_tag,
            'get_notes': self.get_notes,
            'get_note': self.get_note,
            'get_revisions': self.get_revisions,
            'save_note': self.save_note
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
        json_data = flask.request.json
        parent_tag = json_data['parent_tag']
        tag_name = json_data['tag_name']

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
                raise MeAPIAddNotesTagDuplicateNameException('A tag with the name "{name}" already exists within parent tag {tag}'.format(name = tag_name, tag = parent_tag))
            
            # Create a new NoteTag object with the new details
            new_entry = NoteTag(
                parent = parent_tag,
                name = tag_name
            )

            # Add the new entry
            session.add(new_entry)
        
        return ([ 'added' ], 1)
    
    @PageAPI.api_endpoint(endpoint_name = 'delete_tag', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def delete_tag(self, *args, **kwargs):
        """ API endpoint to remove a NoteTag """

        # Get the tag id the user wants to delete
        json_data = flask.request.json
        tag_id = json_data['tag']

        # Find the tag
        with DatabaseSession(commit_on_end = True) as session:
            # Get the session
            tags = session.query(NoteTag).filter(
                NoteTag.id == tag_id
            )

            # Check if we have a tag. If we don't give an error
            if tags.count() != 1:
                raise MeAPIDeleteNotesTagInvalidTagException('Tag with id {id} is not found'.format(id = tag_id))
            
            # Remove all tags from all notes
            notes_tags = session.query(NotesTags).filter(
                NotesTags.tag == tag_id
            ).delete()

            # Delete the session
            session.delete(tags.first())

        return([ 'removed' ], 1)
    
    @PageAPI.api_endpoint(endpoint_name = 'rename_tag', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def rename_tag(self, *args, **kwargs):
        """ API endpoint to rename a NoteTag """

        # Get the tag ID the user wants to change and the new name for the tag
        json_data = flask.request.json
        tag_id = json_data['tag']
        tag_name = json_data['tag_name']

        # Find the tag
        with DatabaseSession(commit_on_end = True) as session:
            # Get the session
            tags = session.query(NoteTag).filter(
                NoteTag.id == tag_id
            )

            # Check if we have a tag. If we don't give an error
            if tags.count() != 1:
                raise MeAPIRenameNotesTagInvalidTagExceptionalueException('Tag with id {id} is not found'.format(id = tag_id))
            
            # Rename the tag from all notes
            tag = tags.first()
            tag.name = tag_name

        return([ 'renamed' ], 1)
    
    @PageAPI.api_endpoint(endpoint_name = 'get_notes', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_notes(self, *args, **kwargs):
        """ The 'get_notes' API endpoint returns notes. If no tag is given, it returns all notes
            that don't have a tag """
        
        # Check if we got a tag
        tag = None
        if 'tag' in kwargs.keys():
            # Tag given
            tag = kwargs['tag']

            # Check if the tag is valid
            with DatabaseSession() as session:
                tags = session.query(NoteTag).filter(NoteTag.id == tag)
                if tags.count() != 1:
                    raise MeAPIGetNotesTagNotValidException('The tag {tag} is not a valid tag'.format(tag = parent))
        
        # Get the notes
        all_note_ids = list()
        with DatabaseSession() as session:
            if tag:
                # Get all IDs for the notes that are in this filter
                all_tagged_notes = session.query(NotesTags.note).filter(NotesTags.tag == tag)
                note_ids = session.query(Note).filter(Note.id.in_(all_tagged_notes))
            else:
                # Get all notes with no tag
                all_tagged_notes = session.query(NotesTags.note)
                note_ids = session.query(Note).filter(Note.id.notin_(all_tagged_notes))

            # Get all the note objects
            all_note_ids = note_ids.all()

            # Get the notecount
            note_count = note_ids.count()
        
        return (all_note_ids, note_count)
    
    @PageAPI.api_endpoint(endpoint_name = 'get_note', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_note(self, *args, **kwargs):
        """ The 'get_note' API endpoint returns a specific note and all it's details. """

        # Check if the user gave us a note and give an error when he didn't
        note = None
        if 'note' in kwargs.keys():
            # Note is given
            note = kwargs['note']

            # Retrieve the note from the database
            with DatabaseSession() as session:
                # Get the note from the database
                note_object = session.query(Note).filter(Note.id == note)

                # Check if we have a note. If we don't, give an error
                if note_object.count() == 1:
                    # We found one note; exactly what we needed. We now need to search for the
                    # revision the user requests. If he doesn't request a specific revision, we take
                    # the last revision.

                    revision_object = session.query(NoteRevision).filter(NoteRevision.note == note)

                    # Get the revision count. We need it later
                    revision_count = revision_object.count()

                    # We set 'last_revision' to True and we remember the ID of this revision. If the
                    # user specifies a revision to load, we check if that ID is the same so we can
                    # determine if he is asking for the last revision.
                    last_revision = True
                    last_revision_id = revision_object.order_by(NoteRevision.id.desc()).first().id

                    # Check if the user requested a specific revision
                    revision = None
                    if 'revision' in kwargs.keys():
                        # Get the revision ID
                        revision = kwargs['revision']

                        # Check if this is the last revision
                        if revision != str(last_revision_id):
                            last_revision = False

                        # User gave a revision. Create a new query object
                        revision_object = revision_object.filter(NoteRevision.id == revision)

                    # Check if we have results. If we don't, we give an error
                    if revision_count > 0:
                        # Order the revisions in the correct order
                        revision_object = revision_object.order_by(NoteRevision.id.desc()).first()

                        # In addition to the 'normal' note, we also return the parsed HTML for the
                        # note. We assume the note is written in Markdown. We use the 'markdown'
                        # package for this. We use a few extensions to this;
                        # - extra
                        #   Adds extra Markdown functions, like tables and fenced code blocks
                        # - toc
                        #   Returns as Table of Contents along with the parsed HTML
                        md = markdown.Markdown(extensions = [ 'extra', 'toc', 'codehilite' ])
                        note_markdown = md.convert(revision_object.text)

                        # We create a object to return with the note, the revision and the metadata
                        # for the note.
                        return_object = {
                            'note': note_object.first(),
                            'revision': revision_object,
                            'metadata': {
                                'revision_count': revision_count,
                                'last_revision': last_revision
                            },
                            'markdown': {
                                'text': note_markdown,
                                'toc': md.toc_tokens
                            }
                        }

                        # Return the note object to the client
                        return([ return_object ], 1)
                    else:
                        if revision:
                            raise MeAPIGetNoteInvalidRevisionExeption('Revision {rev_id} not found for note with ID {id}'.format(rev_id = revision, id = note))
                        else:
                            raise MeAPIGetNoteInvalidRevisionExeption('No revisions found for note with ID {id}'.format(id = note))
                else:
                    raise MeAPIGetNoteInvalidNoteExeption('Note with id {id} is not found'.format(id = note))
        else:
            raise MeAPIGetNoteNoNoteExeption('No note id given')

    @PageAPI.api_endpoint(endpoint_name = 'get_revisions', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_revisions(self, *args, **kwargs):
        """ The 'get_revisions' API endpoint returns revisions for a specific note """

        # Check if the user gave us a note and give an error when he didn't
        note = None
        if 'note' in kwargs.keys():
            note = kwargs['note']

            # Check if the note is valid
            with DatabaseSession() as session:
                notes = session.query(Note).filter(Note.id == note)
                if notes.count() != 1:
                    raise MeAPIGetNoteRevisionsNonExistingNoteExeption('The note {note} is not a valid note'.format(note = note))
            
            # Get the revisions
            all_revisions = list()
            with DatabaseSession() as session:
                # Get all revisions from the database. We only get the 'id' and the 'date' for this
                # note since all other information is not needed. We do this user 'load_only' so
                # SQLalchemy keeps it a object. If we would use the 'with_entities' method of the
                # query, we would get a list as return.
                fields = [ 'id', 'created' ]
                revisions = session.query(NoteRevision).options(load_only(*fields)).filter(NoteRevision.note == note).order_by(desc(NoteRevision.id))
                
                # Get the tagcount
                allrevisions = revisions.count()

                # Get all the tag objects
                all_revisions = revisions.all()
            
            return (all_revisions, allrevisions)
        else:
            raise MeAPIGetNoteRevisionsNoNoteExeption('No note id given')
    
    @PageAPI.api_endpoint(endpoint_name = 'save_note', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def save_note(self, *args, **kwargs):
        """ API endpoint to save a (new) note """

        # TODO: Implement
        json_data = flask.request.json

        return([ 'saved' ], 1)
#---------------------------------------------------------------------------------------------------