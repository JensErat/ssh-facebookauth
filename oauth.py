#!/usr/bin/env python

# (C) 2015-04-01 Jens Erat <email@jenserat.de>
# Licensed under the MIT license
#################
# Configuration #
#################

# URI to redirect to
redirect_uri = 'https://jenserat.github.io/ssh-facebookauth/'
# User ID and password to authenticate system
client_id = ''
client_secret = ''
# OAuth2 URIs
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
# List of privileges should be requested
scope = ['email']
# Where to fetch user information from?
user_info_url = 'https://graph.facebook.com/me?fields=email,first_name'
user_info_field = 'email'
# Define identity as wrapper if not needed
def compliance_wrapper(oauth):
  from requests_oauthlib.compliance_fixes import facebook_compliance_fix
  return facebook_compliance_fix(oauth)
# User greeting
def user_greeting(pamh, user_info):
  from pyfiglet import Figlet
  f = Figlet(font='letter')
  banner = f.renderText('Hi %s!' % user_info['first_name'])

  pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, str("""

-------------------------------------------------------------------

%s

(c) 2015-04-01 Jens Erat <email@jenserat.de>, MIT license
Code on GitHub: https://github.com/JensErat/ssh-facebookauth
-------------------------------------------------------------------
""" % banner)))

########
# Code #
########

# Set up logging
import logging
logging.basicConfig(filename = '/var/log/pam-oauth2.log', filemode = 'a', level = logging.DEBUG, format = '%(asctime)s %(levelname)-8s %(message)s', datefmt = '%d.%m.%Y %H:%M:%S')

# PAM authentication, only overriding authentication
def pam_sm_authenticate(pamh, flags, argv):
  logging.debug('authenticate')
  return http_verify(pamh)

def pam_sm_setcred(pamh, flags, argv):
  logging.debug('setcred')
  return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
  logging.debug('acct_mgmt')
  return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
  logging.debug('open_session')
  return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
  logging.debug('close_session')
  return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
  logging.debug('chauthtok')
  return pamh.PAM_SUCCESS

# Verify against an OAuth2 provider
def http_verify(pamh):
  try:
    # Prepare OAuth2 request
    from requests_oauthlib import OAuth2Session
    oauth = compliance_wrapper(OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope))
    authorization_url, state = oauth.authorization_url(authorization_base_url)

    # Prompt user for performing authentication
    class MessagePrompt():
      msg = ''
      msg_style = 0
    prompt = MessagePrompt()
    prompt.msg = "\n\nPlease authorize at:\n\n%s\n\nThen, paste the redirect URL:\n\n" % authorization_url
    prompt.msg_style = pamh.PAM_PROMPT_ECHO_ON
    response = pamh.conversation(prompt).resp

    # Get token, request user information for identification
    oauth.fetch_token(token_url, client_secret=client_secret, authorization_response=response)
    r = oauth.get(user_info_url)
    logging.debug(r.content)

    # Get user ID, compare against gecos field in passwd file
    user_info = oauth.get(user_info_url).json()
    import pwd
    if set(['ALL_USERS_ALLOWED', user_info[user_info_field]]) & set(pwd.getpwnam(pamh.user).pw_gecos.split(',')):
      user_greeting(pamh, user_info)
      return pamh.PAM_SUCCESS
    else:
      # Authentification failed (wrong user)
      return pamh.PAM_USER_UNKOWN
  except Exception as e:
    # Problem during authentification
    logging.debug(e)
    return pamh.PAM_SYSTEM_ERR
