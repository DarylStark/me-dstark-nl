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

                    // Add the 'content' div to the 'systeminfo' template and convert it to a Jquery
                    // object
                    // TODO: Make a method for this
                    templates['systeminfo'] = $('<div id=\'content\'>' + templates['systeminfo'] + '</div>');

                    // Add the values of the API call to the template for the database
                    templates['systeminfo'].find('#var-database-pool-size').html(data['database']['pool_size']);
                    templates['systeminfo'].find('#var-database-overflow').html(data['database']['overflow']);
                    templates['systeminfo'].find('#var-database-checkedin').html(data['database']['checked_in']);
                    templates['systeminfo'].find('#var-database-checkedout').html(data['database']['checked_out']);

                    // Add the values of the API call to the template for the process
                    templates['systeminfo'].find('#var-process-pid').html(data['process']['pid']);
                    templates['systeminfo'].find('#var-process-username').html(data['process']['username']);
                    templates['systeminfo'].find('#var-process-cpu').html(data['process']['cpu_percentage']);
                    // TODO: Convert the bytes to human readable
                    templates['systeminfo'].find('#var-process-memory').html(data['process']['used_memory']);

                    // Add the values of the API call to the template for the application
                    templates['systeminfo'].find('#var-application-environment').html(data['application']['environment']);
                    templates['systeminfo'].find('#var-application-staticloader').html(data['application']['staticloader_files']);
                    templates['systeminfo'].find('#var-application-templateloader').html(data['application']['templateloader_files']);

                    // Add the values from the client UI
                    templates['systeminfo'].find('#var-client-templateloader').html(Object.keys(Templates.template_cache).length);

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