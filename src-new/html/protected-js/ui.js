/***************************************************************************************************
 * Class for the UI
***************************************************************************************************/
class UI {
    // Static class for the UI of the application. Does all basic functions, like setting the
    // listeners and starting specific pages.

    // The classes to start when the user starts a specific page
    static page_classes = {
        'main_feed': {
            'class': PageFeed
        },
        'main_planning': {
            'class': PagePlanning
        },
        'main_events_concerts': {
            'class': PageConcerts
        }
    };

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
            // Retrieve the class for the requested page
            var menu_item_id = $(this).attr('id');
            var page_class = UI.page_classes[menu_item_id]['class'];

            // Create an instance of the class
            var page = new page_class();

            // Start the 'start' method of the class so the page can be displayed
            page.start();
        });
    }
}
/***************************************************************************************************
 * Main of the script
***************************************************************************************************/
$(document).ready(function() {
    // Initiate the UI
    UI.init();
});
/**************************************************************************************************/