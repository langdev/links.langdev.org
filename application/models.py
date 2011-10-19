"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db
import urllib
import HTMLParser


class Link(db.Model):
  authors = db.StringListProperty(required=True)
  link_url = db.LinkProperty(required=True)

  created_at = db.DateTimeProperty(auto_now_add=True)
  updated_at = db.DateTimeProperty(auto_now_add=True)

  title = db.StringProperty(required=False)

  @property
  def link_text(self):
    try:
      return urllib.unquote(str(self.link_url)).decode('utf-8')
    except UnicodeDecodeError:
    	return str(self.link_url)

  @property
  def link_title(self):
    text = None
    if self.title:
      text = '%s (%s)' % (HTMLParser.HTMLParser().unescape(self.title), self.link_text)
    else:
    	text = '%s' % self.link_text

    return text
    
