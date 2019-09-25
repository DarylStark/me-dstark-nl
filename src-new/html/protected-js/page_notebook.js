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
                if (tag) {
                    newurl = '/ui/notebook/list/' + t.tag;
                } else {
                    newurl = '/ui/notebook/'
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
                    console.log('Note clicked');
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

        // Add them to the UI
        $.each(actionbuttons.reverse(), function(index, actionbutton) {
            if (actionbutton['show']) {
                UI.add_action_button(actionbutton);
            }
        });

        // Set them
        UI.set_action_buttons();
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
        //   Show the overfiew of folder '86' and show note '120'
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
                'action': 'list'
            },
            'list': {
                'regex': /^\/ui\/notebook\/list\/([0-9]+)\/?$/,
                'tag': 1,
                'note': null,
                'action': 'list'
            },
            'show': {
                'regex': /^\/ui\/notebook\/show\/([0-9]+)\/([0-9]+)\/?$/,
                'tag': 1,
                'note': 2,
                'action': 'show'
            },
            'edit': {
                'regex': /^\/ui\/notebook\/edit\/([0-9]+)\/([0-9]+)\/?$/,
                'tag': 1,
                'note': 2,
                'action': 'edit'
            }
        }

        // Set the values for the class to empty so we can overwrite them
        t.tag = null;
        t.note = null;
        
        // Loop through the objects to find the correct action
        $.each(regexes, function(key, object) {
            if (object['regex'].test(url)) {
                // Found the correct regex. Let's get the groups
                var groups = Array.from(url.matchAll(object['regex']))[0]
                
                if (object['tag']) {
                    t.tag = groups[object['tag']];
                }

                if (object['note']) {
                    t.note = groups[object['note']];
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

            // Load the requested folder and display the page
            t.navigate_to_tag(t.tag, false, function() {
                    UI.set_loading_text('Setting content');
                    UI.replace_content(templates['notebook']);
                }
            );
        },
        function() {
            // Something went wrong while requesting the template data
            UI.notification('Couldn\'t retrieve templates', 'Refresh', function() { t.start(); } );
            UI.stop_loading();
        });
    }
};
/**************************************************************************************************/