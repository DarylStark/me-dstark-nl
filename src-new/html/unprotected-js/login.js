function successLogin(data) {
    result = data['result']['data'];
    if (result[0] == 'authenticated') {
        location.href = '/ui';
    } else {
        console.log('Authentication error');
    }
}

function errorLogin() {
    console.log('Google error');
}

function onSuccess(googleUser) {
    // Get the user token for this user
    token = googleUser.getAuthResponse().id_token;

    // Send the token to the verification API
    $.ajax({
        type: 'POST',
        url: '/api/aaa/login',
        data: { token: token },
        success: successLogin,
        error: errorLogin
    });
}

function onFailure(error) {
    console.log(error);
}

function renderButton() {
    gapi.signin2.render('my-signin2', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSuccess,
        'onfailure': onFailure
    });
}

$(document).ready(function() {
    renderButton();
});