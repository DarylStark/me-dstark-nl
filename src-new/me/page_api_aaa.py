#!/usr/bin/env python3
"""
    me - page_api_aaa.py

    API module for '/api/aaa'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me import APIPage
from me import PageAPI
from me_database import *
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy import or_
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
            'verify': self.verify
        }
    
    @PageAPI.api_endpoint(allowed_methods = [ 'post' ])
    def verify(self, *args, **kwargs):
        """ Method to verify the credentials of a logging in users """
        
        # Get the token from the request
        token = flask.request.form.get('token')

        # Get the idinfo for this session
        client_id = '167809871556-j2ghbhtoqaeka5bfpr96nmqrp1f3m897.apps.googleusercontent.com'
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

        # Check if the token is signed correctly
        if idinfo['iss'] not in [ 'accounts.google.com', 'https://accounts.google.com' ]:
            # TODO: Custom error (AuthenticationFailed)
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
            return ( [ 'authenticated' ], 1)
        else:
            # TODO: Custom error (AuthenticationFailed)
            raise ValueError
#---------------------------------------------------------------------------------------------------