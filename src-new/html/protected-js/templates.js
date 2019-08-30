/***************************************************************************************************
 * Class to load Templates
***************************************************************************************************/
class Templates {
    // Static class to load templates from the API and store them in a local cache to increase
    // performance.

    // The template cache
    static template_cache = {}

    static get_templates_callback(cb, templates) {
        // Method to start the callback for 'get_template'. We do this in a seperate method so we
        // can start if from different places without repeating ourselves

        // Empty dict with the templates that the user requested
        var return_templates = {};

        // Create a object with the templates
        $.each(templates, function(index, element) {
            return_templates[element] = Templates.template_cache[element];
        });

        // Start the callback with the requested templates
        cb(return_templates);
    }

    static get_template(templates, cb_succes) {
        // Method that get templates from the API and saves it into the cache. Multiple templates
        // can be given to retrieve more then one template. The 'templates' argument should be an
        // Array

        // Empty array that will contain the needed templates later on
        var needed_templates = new Array();

        // Check which templates we need to retrieve
        $.each(templates, function(index, template) {
            if (!(template in Templates.template_cache)) {
                needed_templates.push(template);
            }
        });

        // Do the API request (if needed)
        if (needed_templates.length > 0) {
            UI.api_call(
                'GET',
                'templates', 'get',
                function(data, status, xhr) {
                    // Got the templates, save them into cache
                    $.each(data['result']['data'][0], function(key, value) {
                        Templates.template_cache[key] = value;
                    });

                    // We have saved the templates. Start the callback
                    Templates.get_templates_callback(cb_succes, templates);
                },
                function() {
                    // Something went wrong while requesting the data
                    // TODO: Enhance this
                    console.log('Failed');
                },
                { templates: needed_templates }
            );
        } else {
            // Templates are loaded, start the callback
            Templates.get_templates_callback(cb_succes, templates);
        }
    }
};
/**************************************************************************************************/