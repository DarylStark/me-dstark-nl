/***************************************************************************************************
 * Main of the script
***************************************************************************************************/
// Handler for when the document is ready loading
$(document).ready(function() {
    // Initiate the UI
    UI.init();

    // Load the GAPI module. We need this to logout
    gapi.load('auth2', function() {
        gapi.auth2.init();
    });
});
/**************************************************************************************************/