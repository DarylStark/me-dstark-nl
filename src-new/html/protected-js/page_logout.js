/***************************************************************************************************
 * Class for the page 'logout'
***************************************************************************************************/
class PageLogout {
    start() {
        // Log the user off from Google (only for this website)
        gapi.auth2.getAuthInstance().signOut().then(function() {
            // Start a request to the API endpoint to log off
            UI.api_call(
                'GET',
                'aaa', 'logout',
                function(data, status, xhr) {
                    // The API request was successfull. Get the data returned from the API
                    var data = data['result']['data'];

                    // Check if the key 'logged out' is in the returned value
                    if ($.inArray('logged out', data) >= 0) {
                        // Redirect the user to the loginpage
                        location.href = '/';
                    }
                },
                function() {
                    // Something went wrong while requesting the data
                    // TODO: Enhance this
                    console.log('Failed');
                }
            );
        });
    }
};
/**************************************************************************************************/