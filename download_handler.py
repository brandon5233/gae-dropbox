from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from directory import Directories
from google.appengine.api import users

import jinja2
import os


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def post(self):

        index = int(self.request.get('index'))
        collection_key = self.request.get('current_cwd_key')
        collection_key = ndb.Key(Directories, collection_key)
        collection = collection_key.get()

        self.send_blob(collection.blobs[index])

