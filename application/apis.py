"""
apis.py

LangDev Links API Handler

"""


from flask import render_template, flash, url_for, redirect, request, jsonify
from decorators import api_auth_required

from models import Link
from datetime import datetime

from google.appengine.api import taskqueue

import hashlib
import logging

@api_auth_required
def post_link():

  link = request.values.get('q')
  author = request.values.get('author')


  key = hashlib.md5(link).hexdigest()
  
  exists = Link.get_by_key_name(key)
  try:
    if not exists:
      link = Link(key_name=key,
                  link_url=link,
                  authors=[author])
      link.put()
      taskqueue.add(url='/_worker/fetch_title', params={ 'url': link, 'key': key })
    else:

      if author not in exists.authors:
        exists.authors.append(author)
        exists.updated_at = datetime.now()
        exists.put()
        taskqueue.add(url='/_worker/fetch_title', params={ 'url': link, 'key': key })

    return jsonify({'result': True})
  except:
    logging.exception('api call failed')
    return jsonify({'result': False})
