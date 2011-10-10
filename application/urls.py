"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template, request, g

from application import app
from application import views
from application import apis
from application import tasks

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from geo_timezone import time_zone_by_country_and_region

from pytz.gae import pytz
## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'index', view_func=views.index)
app.add_url_rule('/<int:year>/<int:month>/<int:day>', 'index', view_func=views.index)

app.add_url_rule('/test', 'test', view_func=views.test)

app.add_url_rule('/api/link', 'api.link', view_func=apis.post_link, methods=('POST',) )

# async worker
app.add_url_rule('/_worker/fetch_title', view_func=tasks.fetch_title, methods=('POST',))

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
  return value.replace(tzinfo=pytz.utc).astimezone(g.tz).strftime(format)

@app.before_request
def guess_tz():
  memcache_key = 'tzg_%s' % request.remote_addr
  data = memcache.get(memcache_key)

  if data is not None:
  	g.tz = _get_tz(data)
  	return

  geo  = ''
  try:
    res = urlfetch.fetch('http://geoip.wtanaka.com/cc/%s' % request.remote_addr)
    if res.status_code == 200:
    	geo = res.content
  except urlfetch.Error, e:
    geo = 'kr'

  if geo:
    memcache.set(memcache_key, geo)
    g.tz = _get_tz(geo)
  else:
  	g.tz = _get_tz()

def _get_tz(tzname=None):

  tz = None
  try:
    tz = pytz.timezone(time_zone_by_country_and_region(geo))
  except:
    tz = pytz.timezone('Asia/Seoul')

  return tz
