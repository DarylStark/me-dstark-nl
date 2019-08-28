/***************************************************************************************************
 * Main of the script
***************************************************************************************************/
// Handler for when the user enters a page via the back button
$(window).on('popstate', function(event){
    // We start the page as we would normally do; via the URL
    UI.start_page_from_url();
});
/**************************************************************************************************/
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