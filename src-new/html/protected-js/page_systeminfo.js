/***************************************************************************************************
 * Class for the page 'system info'
***************************************************************************************************/
class PageSystemInfo {
    // The PageSystemInfo class is used for the 'System information' page. This page displays some
    // system information that can be usefull to the user. It also gives some other options, like
    // emptying the chaches for internal Python classes and emptying the caches for the local UI.

    bytes_to_human_readable(bytes) {
        var thresh = 1024;

        if(Math.abs(bytes) < thresh) {
            return bytes + ' B';
        }
        var units = ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
        var u = -1;
        do {
            bytes /= thresh;
            ++u;
        } while(Math.abs(bytes) >= thresh && u < units.length - 1);

        // Return the new value
        return bytes.toFixed(1) + ' ' + units[u];
    }

    set_var(object, tag_id, value, value_type) {
        // Method to fill a var in the object

        // Check if we need to transform the value
        if (value_type == 'files') {
            // Add 'file' or 'files' to the string
            if (value != 1) {
                value = value.toString() + ' files';
            } else {
                value = value.toString() + ' file';
            }
        } else if (value_type == 'connections') {
            // Add 'connection' or 'conntections' to the string
            if (value != 1 && value != -1) {
                value = value.toString() + ' connections';
            } else {
                value = value.toString() + ' connection';
            }
        } else if (value_type == 'bytes') {
            // Convert a byte-total to human readable format
            value = this.bytes_to_human_readable(value);
        }

        // Replace the var
        object.find('#' + tag_id).html(value);
    }

    reload_data(html_object, callback) {
        // The method that actually reads the data

        UI.start_loading('Retrieving data');

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;
        // Get the system information from /api/system/get_info
        UI.api_call(
            'GET',
            'system', 'get_info',
            function(data, status, xhr) {
                UI.set_loading_text('Parsing data');

                // The API request was successfull. Get the data returned from the API
                var data = data['result']['data'][0];

                // The array with objects for the data we need to set
                var data_set = [
                    { 'tag_id': 'var-database-pool-size', 'data': data['database']['pool_size'], 'value_type': 'connections' },
                    { 'tag_id': 'var-database-overflow', 'data': data['database']['overflow'], 'value_type': 'connections' },
                    { 'tag_id': 'var-database-checkedin', 'data': data['database']['checked_in'], 'value_type': 'connections' },
                    { 'tag_id': 'var-database-checkedout', 'data': data['database']['checked_out'], 'value_type': 'connections' },
                    { 'tag_id': 'var-process-pid', 'data': data['process']['pid'] },
                    { 'tag_id': 'var-process-username', 'data': data['process']['username'] },
                    { 'tag_id': 'var-process-cpu', 'data': data['process']['cpu_percentage'] },
                    { 'tag_id': 'var-process-memory', 'data': data['process']['used_memory'], 'value_type': 'bytes' },
                    { 'tag_id': 'var-application-environment', 'data': data['application']['environment'] },
                    { 'tag_id': 'var-application-staticloader', 'data': data['application']['staticloader_files'], 'value_type': 'files' },
                    { 'tag_id': 'var-application-templateloader', 'data': data['application']['templateloader_files'], 'value_type': 'files' },
                    { 'tag_id': 'var-client-templateloader', 'data': Object.keys(Templates.template_cache).length, 'value_type': 'files' }
                ];

                // Add the values to the object
                $.each(data_set, function(index, object) {
                    t.set_var(
                        html_object,
                        object['tag_id'],
                        object['data'],
                        object['value_type']
                    );
                });

                // Done! Start the callback
                if (callback) {
                    callback();
                }
            },
            function() {
                // Something went wrong while requesting the data
                UI.notification('Couldn\'t retrieve data', 'Refresh', function() { t.start(); } );
                UI.stop_loading();
            }
        );
    }

    start() {
        // Method that gets started when the user requests the page

        // Set the page to loading
        UI.start_loading('Retrieving templates');

        // Set a local var for 'this' that we can re-use in the callbacks
        var t = this;

        // Open the template for the page
        Templates.get_templates(['systeminfo'], function(templates) {
            // Add the 'content' div to the 'systeminfo' template and convert it to a Jquery object
            templates['systeminfo'] = UI.to_jquery(templates['systeminfo'], true);

            // Set the correct loading text
            UI.set_loading_text('Setting action buttons');

            // Add the reload action-button
            var actionbutton = {
                'icon': 'refresh',
                'click': function() { t.reload_data($('#content'), function() { UI.stop_loading(); }) }
            }
            UI.add_action_button(actionbutton);

            // Start the method to retrieve the data
            t.reload_data(templates['systeminfo'], function() {
                UI.set_title('System information');
                UI.set_loading_text('Setting content');
                UI.set_action_buttons();
                UI.replace_content(templates['systeminfo']);
                UI.stop_loading();
            });
        },
        function() {
            // Something went wrong while requesting the template data
            UI.notification('Couldn\'t retrieve templates', 'Refresh', function() { t.start(); } );
            UI.stop_loading();
        });
    }
};
/**************************************************************************************************/