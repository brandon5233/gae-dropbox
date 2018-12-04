from google.appengine.ext import ndb

class Directories(ndb.Model):
    prev_key = ndb.StringProperty()
    prev = ndb.StringProperty()
    dir_name = ndb.StringProperty()
    subdirectory = ndb.StringProperty(repeated=True)
    filenames = ndb.StringProperty(repeated=True)
    blobs = ndb.BlobKeyProperty(repeated=True)
    filetime = ndb.StringProperty(repeated=True)
    star_file = ndb.StringProperty(repeated=True)
    star_folder = ndb.StringProperty(repeated=True)



