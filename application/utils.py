"""

utils.py

Utils

"""

import hmac
import hashlib
import simplejson
import urllib
from google.appengine.api import urlfetch
from secret_keys import LANGDEV_APP_KEY, LANGDEV_SECRET_KEY, LANGDEV_API_KEY
from flask import Response

import logging 


def _langdev_sso_call(user_id, user_pass):
  def hmac_sha1(value):
    hash = hmac.new(LANGDEV_SECRET_KEY, value, hashlib.sha1)
    return hash.hexdigest()
  def hmac_pass(u_pass):
    return hmac_sha1(hashlib.md5(u_pass).hexdigest())

  auth_url = 'http://langdev.org/apps/%s/sso/%s' % (LANGDEV_APP_KEY, user_id)
  auth_data = {'password': hmac_pass(user_pass) }
  result = urlfetch.fetch(url=auth_url,
                          payload=urllib.urlencode(auth_data),
                          method=urlfetch.POST,
                          headers={'Accept': 'application/json'})

  if result.status_code == 200:
    return simplejson.loads(result.content)
  else:
  	return False

def check_langdev_sso(user_id, user_pass):
  """check langdev credentials by sso api"""
  return _langdev_sso_call(user_id, user_pass)

def authenticate():
  """Sends a 401 response"""
  return Response('Langdev Login required', 401, {'WWW-Authenticate': 'Basic realm="Langdev Login"'})

def api_forbidden():
  """Sends a 403 response"""
  return Response('Forbidden', 403)

def check_links_auth(auth, data):

  if not auth:
  	return False

  if not data.has_key('q'):
  	return False

  if not data.has_key('ts'):
  	return False

  ts = data['ts']
  q = data['q']

  logging.info('[API AUTH] try %s with %s %s' % ( auth, ts, q))

  compare_s = '%(api_key)s%(ts)s%(qmd5)s' % { 'ts': ts,
                                              'api_key': LANGDEV_API_KEY, 
                                              'qmd5': hashlib.md5(q).hexdigest() }

  logging.info('[API AUTH] compare_s %s' % compare_s)
  compare_s = '%s' % ( hashlib.md5(compare_s).hexdigest() )
#  logging.info('[API AUTH] second compare_s %s' % compare_s)
  logging.info('[API AUTH] result %s' % str(compare_s==auth))

  return compare_s == auth
