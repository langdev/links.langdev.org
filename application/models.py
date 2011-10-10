"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db
import urllib


class Link(db.Model):
  authors = db.StringListProperty(required=True)
  link_url = db.LinkProperty(required=True)

  created_at = db.DateTimeProperty(auto_now_add=True)
  updated_at = db.DateTimeProperty(auto_now_add=True)

  @property
  def link_text(self):
    return urllib.unquote(str(self.link_url)).decode('utf-8')
