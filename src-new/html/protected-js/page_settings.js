/***************************************************************************************************
 * Class for the page 'settings'
***************************************************************************************************/
class PageSettings {
    constructor() {
        this.old_name = null;
        this.old_email = null;
        this.dirty_name = false;
        this.dirty_email = false;
    }

    save_data() {
        // Method to save the data

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Get the new data
        var name = $('#profile_name').val();
        var email = $('#profile_email').val();

        // TODO: Create API endpoint to save data and call if from here
        
        // Create the data to transmit to the API
        var data = {};
        if (this.dirty_name) { data['name'] = name; }
        if (this.dirty_email) { data['email'] = email; }

        // Save the data (if needed)
        if (Object.keys(data).length) {
            UI.start_loading('Saving data');
            UI.api_call(
                'POST',
                'aaa', 'set_user',
                function(data, status, xhr) {
                    // Set the dirties to False so we know they are not dirty anymore
                    t.dirty_name = false;
                    t.dirty_email = false;

                    // Update the local name and mailaddress
                    t.old_name = name;
                    t.old_email = email;

                    UI.stop_loading();
                },
                function() {
                    // Something went wrong while setting the data
                    UI.notification('Couldn\'t save data', 'Refresh', function() { t.start(); } );
                    UI.stop_loading();
                },
                null,
                data
            );
        }
    }

    start() {
        // Set the page to loading
        UI.start_loading('Retrieving templates');

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Open the template for the page
        Templates.get_templates(['settings', 'settings_session', 'settings_active_session'], function(templates) {
            UI.start_loading('Retrieving user data');

            // Get the user info
            UI.api_call(
                'GET',
                'aaa', 'get_user',
                function(data, status, xhr) {
                    UI.start_loading('Retrieving session data');

                    // Get the user sessions
                    UI.api_call(
                        'GET',
                        'aaa', 'get_sessions',
                        function(sessions, status, xhr) {
                            UI.set_loading_text('Parsing data');

                            sessions = sessions['result']['data'];

                            // Get the data
                            var user = data['result']['data'][0];

                            // Add the 'content' div to the 'systeminfo' template and convert it to a Jquery object
                            templates['settings'] = UI.to_jquery(templates['settings'], true);

                            // Set the data in the object
                            templates['settings'].find('#profile_name').val(user['name']);
                            templates['settings'].find('#profile_email').val(user['email']);
                            t.old_name = user['name'];
                            t.old_email = user['email'];
                            
                            // Add handlers to the 'inputs' so the data gets saved when it loses focus
                            templates['settings'].find('input').focusout(function() {
                                // Get the values
                                var new_name = $('#profile_name').val();
                                var new_email = $('#profile_email').val();

                                // Set the dirty values (if needed)
                                if (new_name != t.old_name) { t.dirty_name = true; } else { t.dirty_name = false; }
                                if (new_email != t.old_email) { t.dirty_email = true; } else { t.dirty_email = false; }

                                // Save the data
                                t.save_data();
                            });

                            // Add the user sessions
                            $.each(sessions, function(index, element) {
                                // Get the correct template; if it is the active session, we need a
                                // different template
                                var template = templates['settings_session'];
                                if (element['current_session']) {
                                    template = templates['settings_active_session'];
                                }

                                // Replace the '{id}' in the template string
                                template = template.replace(new RegExp('{id}', 'g'), element['id']);

                                // Create a new jQuery object for the session-entry
                                var entry = UI.to_jquery(template, false);

                                // Set the name
                                if (element['name']) {
                                    entry.find('#name-' + element['id']).html(element['name']);
                                } else {
                                    entry.find('#name-' + element['id']).html('Unnamed session');
                                }

                                // Set the date
                                var session_date = new Date(element['start'] + ' UTC');
                                entry.find('#date').html(UI.format_datetime(session_date));

                                // Set the IP address
                                entry.find('#address').html(element['ip_address']);

                                // Set the sessionname to the input
                                entry.find('input').val(element['name']);

                                // Add a handler to the title so we can rename it by clicking it
                                entry.find('#name-' + element['id']).click(function() {
                                    var display = $('#rename-' + element['id']).css('display');
                                    if (display == 'none') {
                                        // Slide down the input field
                                        $('#rename-' + element['id']).slideDown(100);

                                        // Set focus to the focus to the textfield
                                        $('#rename-' + element['id']).find('input').focus();
                                    } else {
                                        // Slide it up again
                                        $('#rename-' + element['id']).slideUp(100);
                                    }
                                });

                                // Add a handler to the input; when the user presses ENTER, we save
                                // the new name
                                entry.find('#new_name').on('keyup', function (e) {
                                    if (e.keyCode === 13) {
                                        // Get the new name
                                        var new_name = $('#rename-' + element['id']).find('input').val().trim();
                                        $('#rename-' + element['id']).find('input').val(new_name);

                                        // Create a object for the data
                                        var data = {
                                            'new_name': new_name,
                                            'session': element['id']
                                        };

                                        // Send the new values to the server
                                        UI.start_loading('Saving data');
                                        UI.api_call(
                                            'POST',
                                            'aaa', 'set_session_name',
                                            function() {
                                                // Set the name to the object
                                                if (new_name != '') {
                                                    $('#name-' + element['id']).html(new_name);
                                                } else {
                                                    $('#name-' + element['id']).html('Unnamed session');
                                                }

                                                // Slide the input back up
                                                $('#rename-' + element['id']).slideUp(100);

                                                UI.stop_loading();
                                            },
                                            function() {
                                                UI.notification('Couldn\'t save data', 'Refresh', function() { t.start(); } );
                                                UI.stop_loading();
                                            },
                                            null,
                                            data
                                        );
                                    }
                                });

                                // Add a handler to the button to remove the session
                                entry.find('button').click(function(clicked_element) {
                                    // Check if the button has the confirm class
                                    var confirmed = $(this).hasClass('mdl-button--accent');
                                    
                                    if (!confirmed) {
                                        // Create a object for the data
                                        var data = {
                                            'session': element['id']
                                        };

                                        // Send the new values to the server
                                        UI.start_loading('Removing session');
                                        UI.api_call(
                                            'POST',
                                            'aaa', 'delete_session',
                                            function() {
                                                // Slide the entries up
                                                $('#rename-' + element['id'] + ', #entry-' + element['id']).slideUp(100, function() {
                                                    // Remove the entry
                                                    UI.stop_loading();
                                                });
                                            },
                                            function() {
                                                UI.notification('Couldn\'t remove session', 'Refresh', function() { t.start(); } );
                                                UI.stop_loading();
                                            },
                                            null,
                                            data
                                        );
                                    } else {
                                        $(this).removeClass('mdl-button--accent');
                                        $(this).html('Confirm?');
                                    }
                                });

                                // Append the entry to the correct container
                                templates['settings'].find('#sessions').append(entry);
                            });

                            // Display the page
                            UI.set_title('Settings');
                            UI.set_loading_text('Setting content');
                            UI.set_action_buttons();
                            UI.replace_content(templates['settings']);
                            UI.stop_loading();
                        },
                        function() {
                            // Something went wrong while requesting the data
                            UI.notification('Couldn\'t retrieve session data', 'Refresh', function() { t.start(); } );
                            UI.stop_loading();
                        }
                    );
                },
                function() {
                    // Something went wrong while requesting the data
                    UI.notification('Couldn\'t retrieve data', 'Refresh', function() { t.start(); } );
                    UI.stop_loading();
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