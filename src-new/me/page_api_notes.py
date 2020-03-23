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
            'save_note': self.save_note,
            'delete_note': self.delete_note,
            'remove_tag_from_note': self.remove_tag_from_note,
            'get_tag_tree': self.get_tag_tree,
            'add_tag_to_note': self.add_tag_to_note
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
            
            # Remove the tag from all notes
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
                    if revision_count > 0:
                        last_revision = True
                        last_revision_id = revision_object.order_by(NoteRevision.id.desc()).first().id
                    else:
                        raise MeAPIGetNoteNoRevisionsExeption('Note {id} has no revisions'.format(id = note))

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

                        # We want to return the tags for the note, so we have to retrieve them and
                        # put them in a list of dicts that we can return
                        tags_query = session.query(NotesTags).filter(NotesTags.note == note)
                        tags = [ { 'id': tag.tag, 'name': tag.tag_object.name } for tag in tags_query.all() ]

                        # In addition to the 'normal' note, we also return the parsed HTML for the
                        # note. We assume the note is written in Markdown. We use the 'markdown'
                        # package for this. We use a few extensions to this;
                        # - extra
                        #   Adds extra Markdown functions, like tables and fenced code blocks
                        # - toc
                        #   Returns as Table of Contents along with the parsed HTML
                        # - codehilite
                        #   Make sure code gets highlighted
                        md = markdown.Markdown(extensions = [ 'extra', 'toc', 'codehilite' ])
                        note_markdown = md.convert(revision_object.text)

                        # We create a object to return with the note, the revision and the metadata
                        # for the note.
                        return_object = {
                            'note': note_object.first(),
                            'revision': revision_object,
                            'metadata': {
                                'revision_count': revision_count,
                                'last_revision': last_revision,
                                'tags': tags
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
        """ API endpoint to save notes. This can be either adding notes, or adding a new revision to
            a existing note """
        
        # Get the variables for the request
        json_data = flask.request.json
        text = json_data['text'].strip()
        title = json_data['title'].strip()

        # Create a new revision
        revision = NoteRevision(
            text = text
        )

        # Check if we are editing a note, or creating a new one
        if 'note_id' in json_data.keys():
            # We are editing a note.
            note_id = json_data['note_id']

            with DatabaseSession(commit_on_end = True) as session:
                notes = session.query(Note).filter(Note.id == note_id)

                if notes.count() == 1:
                    # Get the note
                    note = notes.first()

                    # Add the note_id to the revision
                    revision.note = json_data['note_id']

                    # Update the title of the note
                    if note.title != title:
                        note.title = title

                    # Add the new revision
                    session.add(revision)
                else:
                    # Note doesn't exist
                    raise MeAPIEditNonExistingNoteExeption('Note with id {id} does not exist'.format(id = note_id))

            # Return that we saved the new revision
            return (['saved'], 1)
        else:
            # We are create a new note.
            with DatabaseSession(commit_on_end = True) as session:
                # First, we create the Note object and add it to the database
                new_note = Note(title = title)
                session.add(new_note)

                # Push it to the database
                session.flush()
           
                # Next, we add the Note ID to the revision and add the new revision
                revision.note = new_note.id
                session.add(revision)

                # Save the ID for later user
                note_id = new_note.id

                # If we got a tag, we have to add the note to that tag immidiatly
                if 'tag' in json_data:
                    # Check if the tag exists
                    tags = session.query(NoteTag).filter(NoteTag.id == json_data['tag'])

                    # Create a NotesTag with the correct details so we cana dd the note to the tag
                    if tags.count() == 1:
                        note_tag = NotesTags(
                            tag = json_data['tag'],
                            note = note_id
                        )

                        # Add the NotesTag
                        session.add(note_tag)
                    else:
                        raise MeAPIAddNoteInvalidTagExeption('Tag {tag} doesn\'t exist'.format(tag = json_data['tag']))

            # Done! We can return the new ID for the note
            return ([ note_id ], 1)
    
    @PageAPI.api_endpoint(endpoint_name = 'delete_note', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def delete_note(self, *args, **kwargs):
        """ API endpoint to remove a Note """

        # Get the note id the user wants to delete
        json_data = flask.request.json
        note_id = json_data['note']

        # Find the note
        with DatabaseSession(commit_on_end = True) as session:
            # Get the session
            notes = session.query(Note).filter(
                Note.id == note_id
            )

            # Check if we have a note. If we don't give an error
            if notes.count() != 1:
                raise MeAPIDeleteNoteInvalidNoteException('Note with id {id} is not found'.format(id = note_id))
            
            # Remove all revisions for this note
            note_revisions = session.query(NoteRevision).filter(
                NoteRevision.note == note_id
            ).delete()

            # Remove all tags for this note
            notes_tags = session.query(NotesTags).filter(
                NotesTags.note == note_id
            ).delete()

            # Delete the session
            session.delete(notes.first())

        return([ 'removed' ], 1)

    @PageAPI.api_endpoint(endpoint_name = 'remove_tag_from_note', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def remove_tag_from_note(self, *args, **kwargs):
        """ API endpoint to remove a Tag from a Note """

        # Get the note id the user wants to delete
        json_data = flask.request.json
        note_id = json_data['note']
        tag_id = json_data['tag']

        # Find the NoteTag
        with DatabaseSession(commit_on_end = True) as session:
            # Get the session
            notestags = session.query(NotesTags).filter(
                NotesTags.note == note_id,
                NotesTags.tag == tag_id
            )

            # Check if we have a note. If we don't give an error
            if notestags.count() != 1:
                raise MeAPIDeleteNoteTagInvalidNoteException('NotesTag with note {note_id} and tag {tag_id} is not found'.format(
                    note_id = note_id,
                    tag_id = tag_id
                ))
            
            # Remove the NotesTags
            notestags.delete()

        return([ 'removed' ], 1)

    @PageAPI.api_endpoint(endpoint_name = 'get_tag_tree', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def get_tag_tree(self, *args, **kwargs):
        """ API endpoint to get all tags in a tree """

        # Get the tags
        all_tags = list()
        with DatabaseSession() as session:
            # Get all tag from the database
            tags = session.query(NoteTag).order_by(NoteTag.parent)

            # Get all the tag objects
            all_tags = tags.all()
        
        # We have all the tags. We can now create a tree of it. To do this, we create a lambda,
        # which is basically a one-statement method, that gets the children for a specific parent.
        # Withing this lambda, we call the lambda itself to get the childeren for the tag we are
        # now in. This is called 'recursion'.
        get_children = lambda parent: [
            { 'id': x.id, 'name': x.name, 'children': get_children(x.id) }
            for x in all_tags
            if x.parent == parent 
        ]

        # For the tree, we create a root node in which we call the created lambda.
        tree = {
            'name': 'root',
            'id': None,
            'children': get_children(None)
        }
        
        # Return the tree
        return (tree, len(tree))
    
    @PageAPI.api_endpoint(endpoint_name = 'add_tag_to_note', allowed_methods = [ 'post' ], allowed_users = { Me.INTERACTIVE_USERS })
    def add_tag_to_note(self, *args, **kwargs):
        """ API endpoint to add a Tag to a Note """

        # Get the note id the user wants to delete
        json_data = flask.request.json
        note_id = json_data['note']
        tag_id = json_data['tag']

        # Create a Database-session
        with DatabaseSession(commit_on_end = True) as session:
            # Create the NotesTags
            new_notestag = NotesTags(
                tag = tag_id,
                note = note_id
            )
            
            # Add the NotesTags
            session.add(new_notestag)

        return([ 'added' ], 1)
#---------------------------------------------------------------------------------------------------