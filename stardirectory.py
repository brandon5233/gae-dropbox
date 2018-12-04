from google.appengine.ext import ndb


class StarDirectory(ndb.Model):
    dir_name = ndb.StringProperty()
    subdirectory = ndb.StringProperty(repeated=True)
    subdirectory_cwd = ndb.StringProperty(repeated=True)
    filenames = ndb.StringProperty(repeated=True)
    blobs = ndb.BlobKeyProperty(repeated=True)
    filetime = ndb.StringProperty(repeated=True)
    star_file = ndb.StringProperty(repeated=True)
    star_folder = ndb.StringProperty(repeated=True)



