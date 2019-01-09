#---------------------------------------------------------------------------------------------------
# is_logged_in.py
#
# Date: 2019-01-09
#
# Method to check if the user is logged in
#---------------------------------------------------------------------------------------------------
# Global imports
from flask import session
#---------------------------------------------------------------------------------------------------
def is_logged_in():
    """ Method to check if we are logged in. If we are, return True. Else, return False """
    if 'loggedin' in session:
        if session['loggedin'] == True:
            return True
    
    return False
#---------------------------------------------------------------------------------------------------