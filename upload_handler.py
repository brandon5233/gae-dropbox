from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from directory import Directories
import datetime
import  jinja2
import os
from google.appengine.api import users
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        message = ''
        dir_level = int(self.request.get('dir_level'))
        user = self.request.get('user')
        current_cwd_key = self.request.get('current_cwd_key')
        current_cwd = self.request.get('current_cwd')
        prev_cwd_key = self.request.get('prev_cwd_key')
        prev_cwd = self.request.get('prev_cwd')
        list_of_subdirectory = []
        list_of_subdirectoryIDs = []
        list_of_files = []
        list_of_fileIDs = []
        list_of_filetime = []
        list_star_folder = []

        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename
        directory_key = ndb.Key(Directories, current_cwd_key)
        directory = directory_key.get()


        existsFlag = False
        for eachfile in directory.filenames:
            if filename == eachfile:
                message = "file already exists"
                existsFlag = True
                break
        if existsFlag == False:
            directory.blobs.append(upload.key())
            directory.filenames.append(filename)
            unique_id = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
            unique_id = unique_id.replace('-','/')
            directory.filetime.append(unique_id)
            directory.put()

        directory_key = ndb.Key(Directories, current_cwd_key)
        directory = directory_key.get()

        for index, subdirectoryID in enumerate(directory.subdirectory):
            temp = ndb.Key('Directories', subdirectoryID)
            temp = temp.get()
            list_of_subdirectory.append(temp.dir_name)
            list_of_subdirectoryIDs.append(subdirectoryID)
            list_star_folder.append(directory.star_folder[index])

        for index, file in enumerate(directory.filenames):
            list_of_files.append(file)
            list_of_fileIDs.append(directory.blobs[index])
            list_of_filetime.append(directory.filetime[index])

        temp1 = []
        temp2 = []
        for x, y in sorted(zip(list_of_subdirectory, list_of_subdirectoryIDs)):
            temp1.append(x)
            temp2.append(y)
        list_of_subdirectory = temp1
        list_of_subdirectoryIDs = temp2

        formatted_date = [datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M") for x in
                          list_of_subdirectoryIDs]

        template_values = {
            'logout': users.create_logout_url('/'),
            'user': user,
            'current_cwd_key': current_cwd_key,
            'current_cwd': current_cwd,
            'prev_cwd_key': prev_cwd_key,
            'prev_cwd': prev_cwd,
            'message': message,
            'list_of_subdirectory': list_of_subdirectory,
            'list_of_subdirectoryIDs': list_of_subdirectoryIDs,
            'list_star_folder':list_star_folder,
            'formatted_date': formatted_date,
            'list_of_filetime': list_of_filetime,
            'list_of_files': list_of_files,
            'list_of_fileIDs': list_of_fileIDs,
            'dir_level': dir_level,
            'upload_url': blobstore.create_upload_url('/upload_handler'),
        }

        template = JINJA_ENVIRONMENT.get_template('display.html')
        self.response.write(template.render(template_values))

