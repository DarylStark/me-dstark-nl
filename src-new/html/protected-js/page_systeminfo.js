/***************************************************************************************************
 * Class for the page 'system info'
***************************************************************************************************/
class PageSystemInfo {
    // The PageSystemInfo class is used for the 'System information' page. This page displays some
    // system information that can be usefull to the user. It also gives some other options, like
    // emptying the chaches for internal Python classes and emptying the caches for the local UI.

    start() {
        console.log('Starting SystemInfo');

        // Open the template for the page
        Templates.get_templates(['systeminfo'], function(templates) {
            // Get the system information from /api/system/get_info
            UI.api_call(
                'GET',
                'system', 'get_info',
                function(data, status, xhr) {
                    // The API request was successfull. Get the data returned from the API
                    var data = data['result']['data'][0];
                    console.log(data);

                    // Add the 'content' div to the 'systeminfo' template and convert it to a Jquery
                    // object
                    // TODO: Make a method for this
                    templates['systeminfo'] = $('<div id=\'content\'>' + templates['systeminfo'] + '</div>');

                    // Add the values of the API call to the template
                    templates['systeminfo'].find('#var-process-pid').html(data['process']['pid']);

                    // TODO: Upgrade the template (via a method) for MDL

                    // Display the template
                    // TODO: Make a method for this that also removes the old content. Maybe with a
                    // nice effect
                    $('#scroller').append(templates['systeminfo']);
                },
                function() {
                    // Something went wrong while requesting the data
                    // TODO: Enhance this
                    console.log('Failed');
                }
            );
        },
        function() {
            // Something went wrong while requesting the template data
            // TODO: Enhance this
            console.log('Failed');
        });
    }
}
/**************************************************************************************************/