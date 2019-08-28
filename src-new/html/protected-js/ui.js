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
            'default_url': '/ui/feed/'
        },
        'main_planning': {
            'class': PagePlanning,
            'url': /^\/ui\/planning([\/].*|)$/,
            'default_url': '/ui/planning/'
        },
        'main_events_concerts': {
            'class': PageConcerts,
            'url': /^\/ui\/events\/concerts([\/].*|)$/,
            'default_url': '/ui/events/concerts/'
        },
        'user_settings': {
            'class': PageSettings,
            'url': /^\/ui\/settings\/?$/,
            'default_url': '/ui/settings/'
        },
        'user_logout': {
            'class': PageLogout,
            'url': /^\/ui\/logout\/?$/,
            'default_url': '/ui/logout/'
        }
    };
    static default_page_id = 'main_feed';

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

        // Initialization of the page is done, start the correct page based on the URL
        UI.start_page_from_url();
    }

    static start_page_from_id(page_id, update_history = true) {
        // Method to start a specific page from the page_classes dictionary. The 'page_id' will be
        // the key from the dict. In the menus, this will be the 'id' value for the link that is
        // clicked.

        // Get the requested page
        var page = UI.page_classes[page_id];

        // Find the class for the requested page
        var page_class = page['class'];

        // TODO: if the class is not found, give an error

        // Create an instance of the class
        var page_object = new page_class();

        // Update the browser history stack (if needed)
        if (update_history) {
            // TODO: Make sure the history gets only updated if it changes. So if the user is on the
            // feed page and clicks on the 'feed' menu, don't change the history. Maybe don't even
            // change the page itself.
            history.pushState(page['default_url'], '', page['default_url']);
        }

        // Start the 'start' method of the class so the page can be displayed
        page_object.start();
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
}
/**************************************************************************************************/