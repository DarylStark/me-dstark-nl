/***************************************************************************************************
 * Class for the UI
***************************************************************************************************/
class UI {
    // Static class for the UI of the application. Does all basic functions, like setting the
    // listeners and starting specific pages.

    // The classes to start when the user starts a specific page
    static page_classes = {
        'main_feed': {
            'class': PageFeed,
            'url': /^\/ui\/feed([\/].*|)$/,
            'default_url': '/ui/feed/',
            'highlight_item': true
        },
        'main_planning': {
            'class': PagePlanning,
            'url': /^\/ui\/planning([\/].*|)$/,
            'default_url': '/ui/planning/',
            'highlight_item': true
        },
        'main_events_concerts': {
            'class': PageConcerts,
            'url': /^\/ui\/events\/concerts([\/].*|)$/,
            'default_url': '/ui/events/concerts/',
            'highlight_item': true
        },
        'user_systeminfo': {
            'class': PageSystemInfo,
            'url': /^\/ui\/systeminfo\/?$/,
            'default_url': '/ui/systeminfo/',
            'highlight_item': false
        },
        'user_settings': {
            'class': PageSettings,
            'url': /^\/ui\/settings\/?$/,
            'default_url': '/ui/settings/',
            'highlight_item': false
        },
        'user_logout': {
            'class': PageLogout,
            'url': /^\/ui\/logout\/?$/,
            'default_url': '/ui/logout/',
            'highlight_item': false
        }
    };
    static default_page_id = 'main_feed';
    static current_page_id = null;
    static current_page = null;
    static action_buttons = new Array();
    static loading_text = '';

    static init() {
        // Initiator of the User Interface. Sets all listeners where they should be

        // Set a listener to the 'main menu' headers to hide the submenus
        $('#main_menu').children('nav').each(function(element, value) {
            // Set the listener to the button
            $(value).find('button').click(function() {
                // Check if this button is rotated. If it isn't, add the 'rotate' class to the CSS
                // classes. This class will rotate it.
                if ($(this).hasClass('rotated')) {
                    $(this).removeClass('rotated');
                } else {
                    $(this).addClass('rotated');
                }

                // Slide the menu up or down, depending on the current state
                $(value).find('nav#submenu-' + $(value).attr('id')).slideToggle(100);
            });
        });

        // Set listeners to the 'main menu' menuitems themselfs
        $('#main_menu').find('a').click(function() {
            // Retrieve the id for the requested page
            var menu_item_id = $(this).attr('id');
            
            // Start the correct page
            UI.start_page_from_id(menu_item_id);
        });

        // Set listeners to the 'user menu' menuitems
        $('#user_menu').find('li').click(function() {
            // Retrieve the id for the requested page
            var menu_item_id = $(this).attr('id');
            
            // Start the correct page
            UI.start_page_from_id(menu_item_id);
        });

        // Handler for when the user enters a page via the back button
        $(window).on('popstate', function(event){
            // We start the page as we would normally do; via the URL
            UI.start_page_from_url();
        });

        // TODO: Preload templates; the template for the ui_action_button, for example

        // Initialization of the page is done, start the correct page based on the URL
        UI.start_page_from_url();
    }

    static start_page_from_id(page_id, update_history = true) {
        // Method to start a specific page from the page_classes dictionary. The 'page_id' will be
        // the key from the dict. In the menus, this will be the 'id' value for the link that is
        // clicked.
        //
        // If the page the user wants to open is the same as the page that already is open, we skip
        // this method. This way, we can make sure not reloads happen that shouldn't happen

        if (UI.current_page_id != page_id) {
            // Get the requested page
            var page = UI.page_classes[page_id];

            // Find the class for the requested page
            var page_class = page['class'];

            // TODO: if the class is not found, give an error

            // Create an instance of the class
            var page_object = new page_class();

            // Update the browser history stack (if needed)
            if (update_history) {
                history.pushState(page['default_url'], '', page['default_url']);
            }

            // Remove all highlighst
            $('.me-navigation__link_active').removeClass('me-navigation__link_active');

            // Check if we need to highlight the menuitem
            if (page['highlight_item']) {
                $('#' + page_id).addClass('me-navigation__link_active');
            }

            // Set the current page id and set the object to a local var for re-use
            UI.current_page_id = page_id;
            UI.current_page = page_object;

            // Start the 'start' method of the class so the page can be displayed
            page_object.start();
        }
    }

    static start_page_from_url() {
        // Method to start a specific page from the page_classes dictionary based on the URL that is
        // given. Will search in the page_classes for a matching URL using regex and start that
        // specific page.

        // Get the given pathname
        var pathname = window.location.pathname;

        // Set 'found' to false. If it is still false after looking for a regex, we can redirect the
        // user to the default homepage
        var found = false;

        // Loop through the 'page_classes' dict and find a regex that matches
        $.each(UI.page_classes, function(page_id, object) {
            // Get the regex for the page
            var regex = object['url'];

            // Check if the regex matches the pathname
            if (regex.test(pathname)) {
                // It matches! Start the correct page
                UI.start_page_from_id(page_id, false);
                found = true;
            }
        });

        // If we didn't found anything, redirect the user to the default page
        if (!found) {
            UI.start_page_from_id(UI.default_page_id, true);
        }
    }

    static api_call(method, group, endpoint, cb_success, cb_error, variables = null, data = null) {
        // Method to retrieve data from the API. The 'group' and 'endpoint' arguments specify which
        // data to retrieve. The 'variables' argument can be a dict containing the arguments to pass
        // to the API (like page, limit, etc.). The 'data' argument will be data passed to a request
        // if it is a POST request. The type of request (POST, GET, etc.) can be given with the
        // 'method' argument.

        // Construct the URL for the API call
        var url = '/api/' + group + '/' + endpoint;

        // Add the variables (if set)
        if (variables) {
            // Empty array with the key/value pairs
            var url_vars = new Array();

            // Add the key/value pairs
            for (var variable in variables) {
                url_vars.push(variable + '=' + variables[variable]);
            }

            // Add the new variables to the URL
            url += '?' + url_vars.join('&');
        }

        // Create a object for the jQuery options for the 'ajax' call
        var jquery_ajax_options = {
            cache: false,
            dataType: 'json',
            method: method,
            success: function(data, status, xhr) {
                // API Call was a success! Start the given success callback
                if (cb_success) {
                    cb_success(data, status, xhr);
                }
            },
            error: function(data, status, xhr) {
                // API Call was a *not* success! Start the given error callback
                if (cb_error) {
                    cb_error(data, status, xhr);
                }
            }
        }

        // If we have data, add it
        if (data) {
            jquery_ajax_options['data'] = data
        }

        // Do the API call
        $.ajax(url, jquery_ajax_options);
    }

    static replace_content(new_content_obj) {
        // Method to remove the current content container and replace it with a new one

        // Remove the old one
        $('#content').remove();

        // Upgrade the elements in the new content container
        UI.upgrade_elements(new_content_obj);

        // Add the new one
        $('#scroller').append(new_content_obj);
    }

    static add_action_button(button) {
        // Method to add a action button to the actionbutton stack. The buttons get address as soon
        // as the 'set_action_buttons' method is called.

        // Add the button
        UI.action_buttons.push(button);
    }

    static set_action_buttons() {
        // Method to remove all action buttons and set the new ones. At the end of this method, the
        // stack gets emptied

        // Get the template for a action button
        Templates.get_templates(['ui_action_button'], function(templates) {
            // Remove the current buttons
            $('#action_buttons').empty();

            // Add the new buttons
            $.each(UI.action_buttons, function(index, button) {
                // Create a HTML icons
                var html_button = $(templates['ui_action_button']);
                html_button.find('#icon').html(button['icon']);

                // Add the click method
                html_button.click(button['click']);

                // Upgrade the element for MDL
                UI.upgrade_elements(html_button);

                // Add the icon to the correct place
                $('#action_buttons').append(html_button);
            });

            // Empty the stack
            UI.action_buttons = new Array();
        });
    }

    static upgrade_elements(htmlelement) {
        // Method to upgrade elements and it's child elements for MDL

        // Upgrade all parent elements
        htmlelement.each(function(index, element) {
            componentHandler.upgradeElement(element);
        });

        // Upgrade all child elements
        htmlelement.find('*').each(function(index, element) {
            componentHandler.upgradeElement(element);
        });
    }

    static start_loading(text) {
        // Start the loading sequence

        // Set the loading-text
        UI.set_loading_text(text);

        // Display the loading element
        $('#loading').show();
    }

    static set_loading_text(text) {
        // Set the loading-text
        $('#loading-text').html(text);
    }

    static stop_loading() {
        // Stops the loading sequence

        // Hide the loading element
        $('#loading').hide();
    }
}
/**************************************************************************************************/