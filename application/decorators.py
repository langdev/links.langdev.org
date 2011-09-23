"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request
from utils import check_langdev_sso, authenticate, check_links_auth, api_forbidden 
  # code...

def login_required(func):
  """Requires langdev login credentials"""
  @wraps(func)
  def decorate(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_langdev_sso(auth.username, auth.password):
    	return authenticate()
    return func(*args, **kwargs)
  return decorate

def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.is_current_user_admin():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view

def api_auth_required(func):
  """Requires Links API authority"""
  @wraps(func)
  def decorate(*args, **kwargs):
    if not request.headers.has_key('X-LINKS-AUTH') or \
    	 not check_links_auth(request.headers['X-LINKS-AUTH'], request.values):
    	return api_forbidden()
    return func(*args, **kwargs)
  return decorate
