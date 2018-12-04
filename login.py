import datetime

import webapp2
import jinja2
import os
from google.appengine.api import users
from directory import Directories
from myusers import MyUsers
from google.appengine.ext import ndb
from directory_handler import DirectoryHandler
from upload_handler import UploadHandler
from google.appengine.ext import blobstore
from download_handler import DownloadHandler
from stardirectory import StarDirectory


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        list_of_subdirectory = []
        list_of_subdirectoryIDs = []
        list_of_files = []
        list_of_fileIDs = []
        list_of_filetime = []
        list_star_file = []
        list_star_folder = []

        message = ''
        #if a user is already logged in, display his folders
        if user:
            #logout = users.create_logout_url(self.request.uri)
            my_user_key = ndb.Key(MyUsers, user.user_id())
            my_user = my_user_key.get()

            #if it is not the first time he's signing in, display his folders
            if my_user:
                rootDirectory = ndb.Key(Directories, my_user.email)
                rootDirectory = rootDirectory.get()

                for index, subdirectoryID in enumerate(rootDirectory.subdirectory):
                    directory = ndb.Key('Directories', subdirectoryID)
                    directory = directory.get()
                    list_of_subdirectory.append(directory.dir_name)
                    list_of_subdirectoryIDs.append(subdirectoryID)
                    list_star_folder.append(rootDirectory.star_folder[index])

                for index, file in enumerate(rootDirectory.filenames):
                    list_of_files.append(file)
                    list_of_fileIDs.append(rootDirectory.blobs[index])
                    list_of_filetime.append(rootDirectory.filetime[index])

            #if it is his first time signing in, create new myuser and root directory
            else:
                my_user = MyUsers(id = user.user_id(), email=user.email())
                my_user.put()
                rootDirectory = Directories(id = my_user.email)
                rootDirectory.put()
                starfolder = StarDirectory(id = my_user.email)
                starfolder.put()

            temp1 = []
            temp2 = []
            temp3 = []
            #sort folders by name
            for x, y,z in sorted(zip(list_of_subdirectory, list_of_subdirectoryIDs, list_star_folder)):
                temp1.append(x)
                temp2.append(y)
                temp3.append(z)
            list_of_subdirectory = temp1
            list_of_subdirectoryIDs = temp2
            list_star_folder = temp3

            formatted_date = [datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M") for
                              x in list_of_subdirectoryIDs]

            template_values = {
                'logout': users.create_logout_url('/'),
                'user': my_user.email,
                'current_cwd': '/',
                'current_cwd_key':  str(my_user.email),
                'prev_cwd_key': '',
                'prev_cwd':'',
                'message': message,
                'list_of_subdirectory': list_of_subdirectory,
                'list_of_subdirectoryIDs': list_of_subdirectoryIDs,
                'list_star_folder':list_star_folder,
                'formatted_date': formatted_date,
                'list_of_files':list_of_files ,
                'list_of_fileIDs': list_of_fileIDs,
                'list_of_filetime': list_of_filetime,
                'dir_level': 1,
                'upload_url': blobstore.create_upload_url('/upload_handler'),
            }
            template = JINJA_ENVIRONMENT.get_template('display.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
    ('/', Login),
    ('/directory_handler',DirectoryHandler),
    ('/upload_handler', UploadHandler),
    ('/download', DownloadHandler)
], debug=True)
