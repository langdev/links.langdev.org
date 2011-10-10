"""
tasks.py

LangDev Links Asynchronus worker tasks

"""

from flask import request
from google.appengine.api import urlfetch
from models import Link
import re

import logging 

_TITLE_RE_ = re.compile(r"\<title\>(.*)\<\/title\>", re.M | re.I )

def fetch_title():

  url = request.form.get('url')
  key = request.form.get('key')
  link = Link.get_by_key_name(key)

  if not link:
  	return ( "Model %s does not exist" % key ), 404

  result = urlfetch.fetch(url=url,
                          follow_redirects=True,
                          headers={'Accept': 'text/html'},
                          method=urlfetch.HEAD)

  if result.status_code == 200 and \
  	 result.headers.get('Content-Type').startswith('text/html'):

     result = urlfetch.fetch(url=url,
                             follow_redirects=True,
                             headers={'Accept': 'text/html'},
                             method=urlfetch.GET)

     if result.status_code == 200:
       _search = _TITLE_RE_.search(result.content)
       if _search:
         link.title = _search.groups()[0]
         link.put()

         return u'Link %s title updated with %s.' % ( url, link.title), 200
       else:
         return u'Link %s does not have html title', 200
     else:
       return u'Link %s return status %d' % (url, result.status_code), 500
  else:
    return u'Link %s return status %d' % (url, result.status_code), 500
