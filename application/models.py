"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db


class LinkModel(db.Model):
  author_id = db.StringProperty(required=True)
  link_url = db.StringProperty(required=True)

  created_at = db.DateTimeProperty(auto_now_add=True)
  updated_at = db.DateTimeProperty(auto_now_add=True)

