from google.appengine.ext import ndb

class MyUsers(ndb.Model):
    email = ndb.StringProperty()
