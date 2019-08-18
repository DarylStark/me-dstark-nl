#!/usr/bin/env python3
"""
    me - page_api_aaa.py

    API module for '/api/aaa'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import Me
from me import APIPage
from me import PageAPI
from me_database import *
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy import or_
from log import Log
import random
import string
import flask
#---------------------------------------------------------------------------------------------------
@PageAPI.register_api_group('aaa')
class PageAPIAAA(APIPage):
    """ Class that can be called to run the API for aaa """

    def __init__(self):
        """ The initiator for this object sets the API endpoints and the methods that are associated
            with this call. The 'show_page' method in the base class will use that dict to decide
            what to do when a API endpoint gets in """
        
        self._api_endpoints = {
            'login': self.login,
            'logout': self.logout
        }
    
    @PageAPI.api_endpoint(endpoint_name = 'login', allowed_methods = [ 'post' ], allowed_users = { Me.LOGGED_OFF })
    def login(self, *args, **kwargs):
        """ Method to login the credentials of a logging in users """
        
        # Get the token from the request
        token = flask.request.form.get('token')

        # Get the idinfo for this session
        client_id = '167809871556-j2ghbhtoqaeka5bfpr96nmqrp1f3m897.apps.googleusercontent.com'
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

        # Check if the token is signed correctly
        if idinfo['iss'] not in [ 'accounts.google.com', 'https://accounts.google.com' ]:
            # TODO: Custom error (AuthenticationFailed)
            Log.log(severity = Log.NOTICE, module = 'API AAA', message = 'Unauthorized user is trying to login: "{email}".'.format(email = idinfo['email']))
            raise ValueError
        
        # Get the account ID and the e-mailadress
        user_id = idinfo['sub']
        user_email = idinfo['email']

        # Find a useraccount for this Google_ID or this e-mailaddress. If it exists, update it with
        # the new information. If it doesn't, we do nothing.
        session = Database.session()
        users = session.query(User).filter(
            or_(User.email == user_email, User.googleid == user_id)
        )

        if users.count() == 1:
            # We have one user. That's what we needed! Logging in was succesful. Let's check if we
            # have to update anything
            user = users.first()
            if user.googleid != user_id:
                user.googleid = user_id
            if user.email != user_email:
                user.email = user_email
            
            # Create a session so we can keep the user online. We create a random string for this
            # that we keep in our database and in a flask session for the user. When the user
            # returns, we can check this string and find the correct session for it.
            session_key = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits,
                k = 32)
            )

            # Create the UserSession
            new_session = UserSession(
                user = user.id,
                secret = session_key,
                ipv4_address = flask.request.remote_addr
            )

            # Add it to the database
            session.add(new_session)
            session.commit()

            # Update the database
            session.commit()

            # Create the Flask session. First we destroy each session that exists
            flask.session.clear()
            flask.session['key'] = session_key

            # Return the value that we need to return when we successful authenticate
            Log.log(severity = Log.INFO, module = 'API AAA', message = 'Authorized user logged in: "{email}".'.format(email = idinfo['email']))
            return ( [ 'authenticated' ], 1)
        else:
            # TODO: Custom error (AuthenticationFailed)
            Log.log(severity = Log.NOTICE, module = 'API AAA', message = 'Unauthorized user is trying to login: "{email}".'.format(email = idinfo['email']))
            raise ValueError
    
    @PageAPI.api_endpoint(endpoint_name = 'logout', allowed_methods = [ 'get' ], allowed_users = { Me.INTERACTIVE_USERS })
    def logout(self, *args, **kwargs):
        """ Method to logoff a user from the system """

        try:
            # Get the session key from the flask session
            key = flask.session['key']

            # Clear the Flask session and remove the item from the database
            flask.session.clear()

            # Remove the session from the database
            session = Database.session()
            sessions = session.query(UserSession).filter(
                UserSession.secret == key
            )
            if sessions.count() == 1:
                email = sessions.first().user_object.email
                session.delete(sessions.first())

            Log.log(severity = Log.INFO, module = 'API AAA', message = 'User "{email}" logged off'.format(email = email))
            
            # Commit the removal
            session.commit()
            
            # Return a tuple with the successcode
            return ( [ 'logged off'], 1)
        except KeyError:
            # TODO: Custom error (NoLogoutKey)
            Log.log(severity = Log.WARNING, module = 'API AAA', message = 'User without logout key is trying to logoff')
            raise ValueError
#---------------------------------------------------------------------------------------------------