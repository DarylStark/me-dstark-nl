/***************************************************************************************************
 * Class for the page 'notebook'
***************************************************************************************************/
class PageNotebook {
    remove_tag() {
        // Method to remove a tag

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Change the menuitem to a confirmation button
        $('#tag-remove-confirm').slideDown(100);

        // When add a click handler to a button, jQuery actually adds it to the existing handler. So
        // if we do it for a button that already has a handler, it ends up double. For this resaon,
        // we first have to remove the click handler
        $('#confirm-remove-button').unbind('click').bind('click',function() {
            // Remove the tag (if needed)
            if (t.tag) {
                UI.start_loading('Removing tag');

                UI.api_call(
                    'POST',
                    'notes', 'delete_tag',
                    function() {
                        // Navigate to the parent tag
                        t.navigate_to_tag(t.parent_tag);
                    },
                    function() {
                        // Something went wrong while requesting the data
                        UI.notification('Couldn\'t remove tag', 'Refresh', function() { t.start(); } );
                        UI.stop_loading();
                    },
                    null,
                    {
                        'tag': t.tag
                    }
                );
            }
        });
    }

    toggle_rename_tag() {
        // Method to toggle the 'rename_tag' input

        var display = $('#tag-rename').css('display');

        if (display == 'none') {
            // We have to add the 'is-dirty' class to the outer div to make sure the label gets
            // hidden.
            $('#rename_new_name').val(this.tag_name);
            $('#rename_new_name_div').addClass('is-dirty');

            // Tag input is not visible; show it and give the input the name of the tag
            $('#tag-rename').slideDown(100);

            // Select all text in it, so the user can immidiatly start typing a new name
            $('#rename_new_name').select();
        } else {
            // Tag input is visible; hide it again
            $('#tag-rename').slideUp(100);
        }
    }

    rename_tag() {
        // Method to rename a new tag

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        var tag_name = $('#rename_new_name').val();
        UI.start_loading('Renaming tag');

        // Get information for the tag
        UI.api_call(
            'POST',
            'notes', 'rename_tag',
            function() {
                // Reload the folder
                t.load_folder(t.tag, function() {
                    // Hide the element
                    $('#tag-rename').slideUp(100);

                    // Stop loading
                    UI.stop_loading();
                },
                function() {
                    // Hide the element
                    $('#tag-rename').slideUp(100);

                    // Something went wrong while requesting the data
                    UI.notification('Couldn\'t rename tag', 'Refresh', function() { t.start(); } );
                    UI.stop_loading();
                });
            },
            function() {
                // Something went wrong while requesting the data
                UI.notification('Couldn\'t rename tag', 'Refresh', function() { t.start(); } );
                UI.stop_loading();
            },
            null,
            {
                'tag': t.tag,
                'tag_name': tag_name
            }
        );
    }

    toggle_add_tag() {
        // Method to toggle the 'add_tag' input

        var display = $('#tag-input').css('display');

        if (display == 'none') {
            // Tag input is not visible; show it
            $('#tag-input').slideDown(100);
            $('#new_name').focus();
        } else {
            // Tag input is visible; hide it again
            $('#tag-input').slideUp(100);
        }
    }

    add_tag() {
        // Method to add a new tag

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        var tag_name = $('#new_name').val();
        UI.start_loading('Saving tag');

        // Get information for the tag
        UI.api_call(
            'POST',
            'notes', 'add_tag',
            function() {
                // Reload the folder
                t.load_folder(t.tag, function() {
                    // Remove the name and hide the element
                    $('#tag-input').slideUp(100);
                    $('#new_name').val('');

                    // Stop loading
                    UI.stop_loading();
                },
                function() {
                    // Remove the name and hide the element
                    $('#tag-input').slideUp(100);
                    $('#new_name').val('');

                    // Something went wrong while requesting the data
                    UI.notification('Couldn\'t save tag', 'Refresh', function() { t.start(); } );
                    UI.stop_loading();
                });
            },
            function() {
                // Something went wrong while requesting the data
                UI.notification('Couldn\'t save tag', 'Refresh', function() { t.start(); } );
                UI.stop_loading();
            },
            null,
            {
                'parent_tag': t.tag,
                'tag_name': tag_name
            }
        );
    }

    display_browser() {
        // Method to set the items for the browser and empty the browser list again

        UI.start_loading('Formatting browser');

        // Remove all current items
        $('#entries').find('.mdl-card__supporting-text').remove();

        // Hide the 'add' and 'remove' lines
        $('#tag-remove-confirm').hide();
        $('#tag-input').hide();
        $('#tag-rename').hide();

        // Add the items
        $.each(this.browser_list, function(index, item) {
            $('#entries').append(item);
        });

        // Empty the array
        this.browser_list = new Array();

        // Add the action buttons
        this.set_action_buttons();

        // Remove the 'remove tag' button if we are not in a tag
        if (this.tag) {
            $('#delete-tag').show();
            $('#rename-tag').show();
        } else {
            $('#delete-tag').hide();
            $('#rename-tag').hide();
        }
    }

    set_title(foldername = null) {
        // Method to set the page title
        if (foldername) {
            UI.set_title('Notebook / ' + foldername);
            $('#browser_title').html(foldername);
        } else {
            UI.set_title('Notebook');
            $('#browser_title').html('Browser');
        }
    }

    load_folder(folder, cb_success, cb_error) {
        // Method to load a specific folder. Before we can load the folders and tags for this
        // folder, we have to get the tag information like the name and it's parent. We only have to
        // do this when a folder is specified; if we are in the root, non of this is interesting.

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        UI.start_loading('Retrieving data for tag');

        if (folder && folder != 0) {
            // Get information for the tag
            UI.api_call(
                'GET',
                'notes', 'get_tag',
                function(data, status, xhr) {
                    // We got the data
                    var tag_info = data['result']['data'][0];

                    // Load the folders for this folder
                    t.load_folder_folders(folder, tag_info['parent'], tag_info['parent_name'], function() {
                        t.load_folder_notes(folder, function() {
                            // Execute the success-callback
                            cb_success();

                            t.parent_tag = tag_info['parent'];
                            t.tag_name = tag_info['name'];

                            // Set the title
                            t.set_title(tag_info['name']);

                            // Display the browser
                            t.display_browser();

                            // Stop loading
                            UI.stop_loading();
                        },
                        cb_error);
                    }, cb_error);
                },
                function() {
                    cb_error();
                },
                { 'tag': folder }
            );
        } else {
            this.load_folder_folders(folder, null, null, function() {
                t.load_folder_notes(folder, function() {
                    // Execute the success-callback
                    cb_success();

                    // Set the title
                    t.set_title();

                    // Display the browser
                    t.display_browser();

                    // Stop loading
                    UI.stop_loading();
                },
                cb_error);
            }, cb_error);
        }
    }

    load_folder_folders(folder, parent, parent_name, cb_success, cb_error) {
        // Method to load folders from the database and display them

        UI.start_loading('Retrieving tags');

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Check if we have a folder to show
        if (folder && folder != 0) {
            var data = { 'parent': folder }
        }

        Templates.get_templates(['notebook_back'], function(templates) {
            if (folder) {
                // Convert the 'notebook_back' to a jQuery object
                var back = UI.to_jquery(templates['notebook_back'], false);

                // Set then name of the parent
                if (parent_name) {
                    back.find('#title').html(parent_name);
                } else {
                    back.find('#title').html('Root');
                }

                // Set a click handler
                back.click(function() {
                    t.navigate_to_tag(parent);
                });

                // Add it to the list (should be the first one)
                t.browser_list.push(back);
            }

            // Get the tags within this tag
            UI.api_call(
                'GET',
                'notes', 'get_tags',
                function(data, status, xhr) {
                    // Display the folders in the browser
                    t.add_folders(data['result']['data'], function() {
                        // Execute the users callback
                        cb_success(data);
                    });
                },
                function() {
                    cb_error();
                },
                data
            );
        },
        function() {
            cb_error();
        });
    };

    load_folder_notes(folder, cb_success, cb_error) {
        // Method to load notes from the database and display them

        UI.start_loading('Retrieving notes for this tag');

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Check if we have a folder to show
        if (folder && folder != 0) {
            var data = { 'tag': folder }
        }

        // Get the notes within this tag
        UI.api_call(
            'GET',
            'notes', 'get_notes',
            function(data, status, xhr) {
                // Display the folders in the browser
                t.add_notes(data['result']['data'], function() {
                    // Execute the users callback
                    cb_success();
                });
            },
            function() {
                cb_error();
            },
            data
        );
    }

    navigate_to_tag(tag, update_url = true, cb_success = null) {
        // Method to navigate to a specific tag. Usuable after a user clicks on a folder in the
        // browser

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Set the tag in the local object
        this.tag = tag;

        // Load the folder
        this.load_folder(this.tag, function(data) {
            // Change the URL, if needed
            if (update_url) {
                var newurl = null;

                if (t.note) {
                    if (tag) {
                        newurl = '/ui/notebook/show/' + t.tag + '/' + t.note;
                    } else {
                        newurl = '/ui/notebook/show/0/' + t.note;
                    }
                    if (t.revision) { newurl += '/' + t.revision; }
                } else {
                    if (tag) {
                        newurl = '/ui/notebook/list/' + t.tag;
                    } else {
                        newurl = '/ui/notebook/'
                    }
                }
                if (newurl) {
                    history.pushState(newurl, '', newurl);
                }
            }

            // If a callback is given, execute it
            if (cb_success) {
                cb_success();
            } else {
                // Stop loading
                UI.stop_loading();
            }
        },
        function() {
            // Something went wrong while requesting the data
            UI.notification('Couldn\'t retrieve tags', 'Refresh', function() { t.start(); } );
            UI.stop_loading();
        });
    };

    add_folders(folders, cb_success) {
        // Method to add the folders to the browser list

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        UI.start_loading('Retrieving template for notebook folders');
        
        Templates.get_templates(['notebook_folder'], function(templates) {
            $.each(folders, function(index, folder) {
                // Create a new object from the template
                var tpl = templates['notebook_folder'];
                var entry = UI.to_jquery(tpl, false);

                // Append the title
                entry.find('#title').html(folder['name']);

                // Add a handler when the user clicks the foldername
                entry.click(function() {
                    t.navigate_to_tag(folder['id']);
                });

                // Add the entry to the list
                t.browser_list.push(entry);
            });

            // Run the callback
            cb_success();
        },
        function() {
            // Something went wrong while requesting the template data
            UI.notification('Couldn\'t retrieve templates', 'Refresh', function() { t.start(); } );
            UI.stop_loading();
        });
    }

    add_notes(notes, cb_success) {
        // Method to add the notes to the browser list

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        UI.start_loading('Retrieving template for notebook notes');
        
        Templates.get_templates(['notebook_note'], function(templates) {
            $.each(notes, function(index, note) {
                // Create a new object from the template
                var tpl = templates['notebook_note'];
                var entry = UI.to_jquery(tpl, false);

                // Append the title
                entry.find('#title').html(note['title']);

                // Add a handler when the user clicks the note
                entry.click(function() {
                    t.get_note(note['id']);
                });

                // Add the entry to the list
                t.browser_list.push(entry);
            });

            // Run the callback
            cb_success();
        },
        function() {
            // Something went wrong while requesting the template data
            UI.notification('Couldn\'t retrieve templates', 'Refresh', function() { t.start(); } );
            UI.stop_loading();
        });
    }

    show_revision_browser() {
        // Method to show the revision browser

        // Set for the callbacks
        var t = this;

        // Get the revision from the API
        UI.start_loading('Retrieving revisions for this note');

        UI.api_call(
            'GET',
            'notes', 'get_revisions',
            function(data, status, xhr) {
                Templates.get_templates(['notebook_revision'], function(templates) {

                    // Remove all revisions from the list
                    $('#revision-items').find('.mdl-card__supporting-text').remove();

                    // Add all revisions to the list
                    $.each(data['result']['data'], function(index, revision) {
                        // Create a new object from the template
                        var tpl = templates['notebook_revision'];
                        var entry = UI.to_jquery(tpl, false);

                        // Append the date
                        var revision_date = new Date(revision['created']);
                        entry.find('#date').html(UI.format_datetime(revision_date));

                        // Append a click event to the note
                        entry.click(function() {
                            t.revision = revision['id'];
                            t.get_note(t.note, revision['id']);
                        });

                        // Add the entry to the revision list
                        $('#revision-items').append(entry);
                    });
                    
                    // Show the revision browser
                    $('#revision-browser').show();

                    // Stop the loading screen
                    UI.stop_loading();
                },
                function() {
                    // Something went wrong while requesting the template data
                    UI.notification('Couldn\'t retrieve templates', 'Refresh', function() { t.start(); } );
                    UI.stop_loading();
                });
            },
            function() {
                // Something went wrong while requesting the data
                UI.notification('Couldn\'t retrieve revisions', 'Refresh', function() { t.start(); } );
                UI.stop_loading();
            },
            null,
            {
                'note': t.note
            }
        );
    }

    get_note(note_id, revision = null, jquery_object = null, cb) {
        // Method to retrieve a note and all it's details from the API

        // Start the loading
        UI.start_loading('Loading note');

        // Set for the callbacks
        var t = this;

        // Get the note from the API
        var api_options = {
            'note': note_id
        }

        // If a revision is given, we add it to the API options
        if (revision) { api_options['revision'] = revision; }

        // Do the API call
        UI.api_call(
            'GET',
            'notes', 'get_note',
            function(data, status, xhr) {
                UI.start_loading('Displaying note');

                // Get the correct object
                var obj = null;
                if (jquery_object) {
                    obj = jquery_object;
                } else {
                    obj = $(document);
                }

                // Remove the revision browser, but only if no revision is given. If a revision is given,
                // the user probably wants the revision browser to stay in screen since he is picking one
                // from the revision browser
                if (revision == null) {
                    t.hide_revision_browser();
                    t.revision = null;
                }

                // Update the URL. We only do this if needed
                if (!cb) {
                    var url_tag = 0;
                    if (t.tag) { url_tag = t.tag; }
                    var url_note = note_id;
                    var newurl = '/ui/notebook/show/' + url_tag + '/' + url_note;
                    if (t.revision) { newurl += '/' + t.revision; }
                    history.pushState(newurl, '', newurl);
                }

                // Set the note in the object
                t.note = note_id;

                // Get the note
                var note = data['result']['data'][0];

                // Get the correct word for 'revisions'
                var revision_word = 'revision'
                if (note['metadata']['revision_count'] > 1) { revision_word = 'revisions';}

                // Split the datetime field
                var revision_date = new Date(note['revision']['created']);

                // Set the correct objects for the note
                obj.find('#note-preview-title').html(note['note']['title']);
                obj.find('#note-preview-note').html(note['markdown']['text']);
                obj.find('#note-notification').hide();
                obj.find('#note-preview').show();
                obj.find('#revision-count').html(note['metadata']['revision_count'] + ' ' + revision_word);
                obj.find('#revision-date').html(UI.format_datetime(revision_date));
                obj.find('#revision-time').html(note['revision']['created']);

                // Add a handler to the 'revisions' button so we can switch revisions if needed. We
                // remove the handler first to make sure there is nothing attached; otherwise it'll
                // do it twice for the second note, three times for the third, etc.
                obj.find('#revision-count').unbind('click');
                obj.find('#revision-count').click(function () { t.show_revision_browser(); });

                // Update the action buttons
                t.set_action_buttons();

                // If we have a callback, process it now
                if (cb) {
                    cb();
                } else {
                    UI.stop_loading();
                }
            },
            function() {
                // Something went wrong while requesting the data
                UI.notification('Couldn\'t open note', 'Refresh', function() { t.start(); } );
                UI.stop_loading();
            },
            null,
            api_options
        );
    }

    edit_note(note_id, revision_id) {
        // Method to start editing a note

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        UI.start_loading('Loading note');

        // Get the note from the API
        var api_options = {
            'note': note_id
        }

        // If a revision is given, we add it to the API options
        if (revision_id) { api_options['revision'] = revision_id; }

        // Do the API call
        UI.api_call(
            'GET',
            'notes', 'get_note',
            function(data, status, xhr) {
                UI.start_loading('Displaying note');

                // Set the text of the note into the text-area
                $('#edit-note-textarea').val(data['result']['data'][0]['revision']['text']);
                $('#edit-note-title').val(data['result']['data'][0]['note']['title']);
                
                console.log(data['result']['data'][0]['metadata']['last_revision']);
                if (data['result']['data'][0]['metadata']['last_revision']) {
                    $('#me-note-edit-revision-warning').hide()
                } else {
                    $('#me-note-edit-revision-warning').show()
                }

                // Remove the divs that are in place now
                $('#note').hide();
                $('#note-notification').hide();
                $('#note-preview').hide();

                // Set our own div
                $('#note-edit').show();
                t.resize_textarea();

                UI.stop_loading();
            },
            function() {
                // Something went wrong while requesting the data
                UI.notification('Couldn\'t open note', 'Refresh', function() { t.start(); } );
                UI.stop_loading();
            },
            null,
            api_options
        );
    }

    set_action_buttons() {
        // Method to set the correct action buttons

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Define the needed action buttons
        var actionbuttons = [
            {
                'icon': 'add',
                'click': function(){},
                'show': true
            }
        ]

        // If we are on a 'note', we have to add the 'edit' button
        if (t.note) {
            actionbuttons.push({
                'icon': 'delete',
                'click': function(){},
                'show': true
            },
            {
                'icon': 'edit',
                'click': function(){
                    t.edit_note(t.note, t.revision);
                },
                'show': true
            });
        }

        // Add them to the UI
        $.each(actionbuttons.reverse(), function(index, actionbutton) {
            if (actionbutton['show']) {
                UI.add_action_button(actionbutton);
            }
        });

        // Set them
        UI.set_action_buttons();
    }

    hide_revision_browser() {
        // Method to hide the revision browser
        // Hide the browser
        $('#revision-browser').hide();
                
        // Remove all revisions from the list
        $('#revision-items').find('.mdl-card__supporting-text').remove();
    }

    resize_textarea() {
        // Method to resize the textarea to the lenght of the text inside of it
        $('#edit-note-textarea').css('height', '5px');
        $('#edit-note-textarea').css('height', $('#edit-note-textarea')[0].scrollHeight);
    }

    start() {
        // Set the page to loading
        UI.start_loading('Retrieving templates');

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Set an empty list of items for the browser
        this.browser_list = new Array();

        // The URL can be build into different ways:
        //
        // - /ui/notebook/
        //   Show the overview of the parent folder without showing a note
        //
        // - /ui/notebook/list/86/
        //   Show the overview of the folder '86' without showing a note
        //
        // - /ui/notebook/show/86/120
        //   Show the overview of folder '86' and show note '120'
        //
        // - /ui/notebook/edit/86/120
        //   Edit the note with the ID 120. The 86 is the ID of the folder in which the note was
        //   before the 'edit' button was clicked. This is important so we can give the correct
        //   'back' link.
        //
        // In the next bit of code, we are going to define the correct regular expressions for the
        // URLs above
        var url = window.location.pathname;
        var regexes = {
            'no_actions': {
                'regex': /^\/ui\/notebook\/?$/,
                'tag': null,
                'note': null,
                'revision': null,
                'action': 'list'
            },
            'list': {
                'regex': /^\/ui\/notebook\/list\/([0-9]+)\/?$/,
                'tag': 1,
                'note': null,
                'revision': null,
                'action': 'list'
            },
            'show': {
                'regex': /^\/ui\/notebook\/show\/([0-9]+)\/([0-9]+)(\/([0-9]+))?\/?$/,
                'tag': 1,
                'note': 2,
                'revision': 4,
                'action': 'show'
            },
            'edit': {
                'regex': /^\/ui\/notebook\/edit\/([0-9]+)\/([0-9]+)\/?$/,
                'tag': 1,
                'note': 2,
                'revision': null,
                'action': 'edit'
            }
        }

        // Set the values for the class to empty so we can overwrite them
        t.tag = null;
        t.note = null;

        // Loop through the objects to find the correct action
        $.each(regexes, function(key, object) {
            if (object['regex'].test(url)) {
                // Found the correct regex. Let's get the groups. For some weird reason i cannot
                // explain, we have to make the RegExp object global with the 'g' flag for Chrome
                // on Android.
                var groups = Array.from(url.matchAll(RegExp(object['regex'], 'g')))[0]
              
                if (object['tag']) {
                    t.tag = groups[object['tag']];
                    if (t.tag == '0' || t.tag == 0) {
                        t.tag = undefined;
                    }
                }

                if (object['note']) {
                    t.note = groups[object['note']];
                }

                if (object['revision']) {
                    t.revision = groups[object['revision']];
                }
            }
        });

        // Open the template for the page
        Templates.get_templates(['notebook', 'notebook_folder'], function(templates) {
            UI.start_loading('Retrieving tags');

            // Add the 'content' div to the 'notebook' template and convert it to a Jquery object
            templates['notebook'] = UI.to_jquery(templates['notebook'], true);

            // Add the handler to the button for adding tags and hide the input
            templates['notebook'].find('#add-tag').click(t.toggle_add_tag);
            templates['notebook'].find('#tag-input').hide();

            // Add the handler to the remove tag button
            templates['notebook'].find('#delete-tag').click(function() { t.remove_tag(); });
            templates['notebook'].find('#tag-remove-confirm').hide();

            // Add the handler to the button for renaming tags and hide the input
            templates['notebook'].find('#rename-tag').click(function() { t.toggle_rename_tag(); });
            templates['notebook'].find('#tag-rename').hide();

            // Hide the 'note preview' and the 'revision-browser'. We will show this again when the
            // user opens a note or opens the revision browser. If the user tries to open a revision
            // from the URL, we do not hide the 'revision-browser'.
            templates['notebook'].find('#note-preview').hide();
            templates['notebook'].find('#revision-browser').hide();
            templates['notebook'].find('#note-edit').hide();

            // Add a resize handler on the edit-note text-area
            templates['notebook'].find('#edit-note-textarea').on('input', function() {
                t.resize_textarea();
            });

            // Add a handler to the 'close-revision-browser' button
            templates['notebook'].find('#close-revision-browser').click(function() {
                t.hide_revision_browser();
            });

            // Add a handler to the 'close-note' button
            templates['notebook'].find('#close-note').click(function() {
                // If the user presses the 'X' on top of a note-preview, the note has to be closed

                // Set the note to undefined
                t.note = undefined;

                // Remove the note-preview
                $('#note-preview').hide();

                // Update the actions buttons
                t.set_action_buttons();

                // Remove the revision browser
                t.hide_revision_browser();

                // Show the note-notification
                $('#note-notification').show();

                // Update the URL
                if (t.tag) {
                    var newurl = '/ui/notebook/list/' + t.tag;
                } else {
                    var newurl = '/ui/notebook/'
                }
                history.pushState(newurl, '', newurl);
            });

            // Add a handler to the input field for new tags when pressing the ENTER key
            templates['notebook'].find('#new_name').on('keyup', function (e) {
                if (e.keyCode === 13) {
                    t.add_tag();
                }
            });

            // Add a handler to the input field for renaming tags when pressing the ENTER key
            templates['notebook'].find('#rename_new_name').on('keyup', function (e) {
                if (e.keyCode === 13) {
                    t.rename_tag();
                }
            });

            // Hide the 'note'
            templates['notebook'].find('#note').hide();

            // If a note is given, display it
            if (t.note) {
                var revision = null;
                if (t.revision) {
                    revision = t.revision;
                }
                t.get_note(t.note, revision, templates['notebook'], function() {
                    // Load the requested folder and display the page
                    t.navigate_to_tag(t.tag, false, function() {
                        UI.set_loading_text('Setting content');
                        UI.replace_content(templates['notebook']);
                        if (t.revision) { t.show_revision_browser(); }
                    });
                });
            } else {
                // Load the requested folder and display the page
                t.navigate_to_tag(t.tag, false, function() {
                    UI.set_loading_text('Setting content');
                    UI.replace_content(templates['notebook']);
                });
            }
        },
        function() {
            // Something went wrong while requesting the template data
            UI.notification('Couldn\'t retrieve templates', 'Refresh', function() { t.start(); } );
            UI.stop_loading();
        });
    }
};
/**************************************************************************************************/