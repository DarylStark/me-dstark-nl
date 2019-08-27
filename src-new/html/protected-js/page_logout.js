/***************************************************************************************************
 * Class for the page 'logout'
***************************************************************************************************/
class PageLogout {
    start() {
        // Log the user off from Google (only for this website)
        gapi.auth2.getAuthInstance().signOut().then(function() {
            // Start a request to the API endpoint to log off
            $.ajax('/api/aaa/logout', {
                cache: false,
                dataType: 'json',
                method: 'GET',
                success: function(data, status, xhr) {
                    // The API request was successfull. Get the data returned from the API
                    var data = data['result']['data'];

                    // Check if the key 'logged out' is in the returned value
                    if ($.inArray('logged out', data) >= 0) {
                        // Redirect the user to the loginpage
                        location.href = '/';
                    }
                },
                error: function()
                {
                    // TODO: Enhance this
                    console.log('Failed');
                }
            });
        });
    }
}
/**************************************************************************************************/