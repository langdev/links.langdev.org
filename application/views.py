"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect
from decorators import login_required

from models import Link
from datetime import datetime, timedelta

@login_required
def index(year=None,month=None,day=None):
  if not year or not month or not day:
  	day = datetime.now()
  else:
  	day = datetime(year, month, day, 0, 0, 0)

  links = Link.all()

  day_from = datetime(day.year, day.month, day.day, 0, 0, 0) 
  day_end = day_from + timedelta(days=1)

  links.filter("updated_at >=", day_from)
  links.filter("updated_at <", day_end)
  links.order("-updated_at")
  return render_template('index.html', links=links, view_today=day)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''


def test():
  link = Link(authors=['kkung','dahlia'], link_url='http://links.langdev.org')
  link.put()
