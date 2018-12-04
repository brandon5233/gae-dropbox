import webapp2
import jinja2
import os
import datetime
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from stardirectory import StarDirectory
from directory import Directories
from google.appengine.ext import blobstore
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class DirectoryHandler(webapp2.RequestHandler):
    def get(self):
        #opens bookmarks folder
        list_of_subdirectory = []
        list_of_subdirectoryIDs = []
        list_of_files = []
        list_of_fileIDs = []
        list_of_filetime = []
        list_star_folder = []
        subdirectory_cwd = []

        user = users.get_current_user()
        user = user.email()
        directory_key = ndb.Key(StarDirectory, user)
        directory = directory_key.get()

        for index, subdirectoryID in enumerate(directory.subdirectory):
            temp = ndb.Key('Directories', subdirectoryID)
            temp = temp.get()
            list_of_subdirectory.append(temp.dir_name)
            list_of_subdirectoryIDs.append(subdirectoryID)
            list_star_folder.append("True")
            subdirectory_cwd.append(directory.subdirectory_cwd[index])

        for index, file in enumerate(directory.filenames):
            list_of_files.append(file)
            list_of_fileIDs.append(directory.blobs[index])
            list_of_filetime.append(directory.filetime[index])

        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []
        for x, y, z, z1 in sorted(
                zip(list_of_subdirectory, list_of_subdirectoryIDs, list_star_folder, subdirectory_cwd)):
            temp1.append(x)
            temp2.append(y)
            temp3.append(z)
            temp4.append(z1)
        list_of_subdirectory = temp1
        list_of_subdirectoryIDs = temp2
        list_star_folder = temp3
        subdirectory_cwd = temp4

        template_values = {
            'logout': users.create_logout_url('/'),
            'user': user,
            'current_cwd_key': directory.key.id(),
            'current_cwd': 'Bookmarks/',
            'prev_cwd_key': '',
            'prev_cwd': '',
            'message': '',
            'list_of_subdirectory': list_of_subdirectory,
            'list_of_subdirectoryIDs': list_of_subdirectoryIDs,
            'list_star_folder': list_star_folder,
            'formatted_date': '',
            'list_of_filetime': list_of_filetime,
            'list_of_files': list_of_files,
            'list_of_fileIDs': list_of_fileIDs,
            'dir_level': 1,
            'upload_url': blobstore.create_upload_url('/upload_handler'),
            'subdirectory_cwd': subdirectory_cwd
        }

        template = JINJA_ENVIRONMENT.get_template('display.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
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
        subdirectory_cwd = []

        if action == 'Add Folder':
            logging.info('Add Folder')
            dir_name = self.request.get('dir_name')
            dir_name = dir_name.strip()
            logging.info(dir_name)

            directory_key = ndb.Key(Directories, current_cwd_key)
            directory = directory_key.get()

            if dir_name == '':
                message = "Please enter a name"
            else:
                exists_flag = False
                for subdirectoryID in directory.subdirectory:
                    temp = ndb.Key(Directories, subdirectoryID)
                    temp = temp.get()
                    if temp.dir_name == dir_name:
                        exists_flag = True
                if exists_flag:
                    message = 'Sorry, directory with that name exists'
                else:
                    unique_id = str(datetime.datetime.now())
                    new_directory = Directories(id=unique_id)
                    new_directory.dir_name = dir_name
                    new_directory.prev_key = current_cwd_key
                    new_directory.prev = current_cwd
                    new_directory.put()

                    directory.subdirectory.append(str(new_directory.key.id()))
                    directory.star_folder.append("False")
                    directory.put()

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

        '''if action == 'Refresh':
            logging.info('Refresh')

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
                list_of_filetime.append(directory.filetime[index])'''



        if action == 'Open Folder':
            logging.info('Open Folder')
            clicked_dir = self.request.get('clicked_dir')
            logging.info(clicked_dir)

            directory_key = ndb.Key(Directories, clicked_dir)
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

            current_cwd_key = clicked_dir
            removeBookmarks = current_cwd.split("/")
            newlist = [x if x!='' else x for x in removeBookmarks ]

            yy = newlist[0].replace('u', '')
            if yy == 'Bookmarks':
                del newlist[0]
            print(newlist)
            for x in newlist:
                current_cwd = current_cwd + x
            current_cwd = current_cwd+directory.dir_name+"/"
            prev_cwd_key = current_cwd_key
            prev_cwd = current_cwd

            dir_level = dir_level + 1

        if action == 'Open Star Folder':
            logging.info('Open Star Folder')

            directory_key = ndb.Key(StarDirectory, user)
            directory = directory_key.get()

            for index, subdirectoryID in enumerate(directory.subdirectory):
                temp = ndb.Key('Directories', subdirectoryID)
                temp = temp.get()
                list_of_subdirectory.append(temp.dir_name)
                list_of_subdirectoryIDs.append(subdirectoryID)
                list_star_folder.append("True")
                subdirectory_cwd.append(directory.subdirectory_cwd[index])

            for index, file in enumerate(directory.filenames):
                list_of_files.append(file)
                list_of_fileIDs.append(directory.blobs[index])
                list_of_filetime.append(directory.filetime[index])

            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            for x, y, z, z1 in sorted(
                    zip(list_of_subdirectory, list_of_subdirectoryIDs, list_star_folder, subdirectory_cwd)):
                temp1.append(x)
                temp2.append(y)
                temp3.append(z)
                temp4.append(z1)
            list_of_subdirectory = temp1
            list_of_subdirectoryIDs = temp2
            list_star_folder = temp3
            subdirectory_cwd = temp4

        if action == 'Delete':
            logging.info('Delete')
            clicked_dir_ID = self.request.get('clicked_dir')
            clicked_dir_key = ndb.Key(Directories, clicked_dir_ID)
            clicked_dir = clicked_dir_key.get()

            current_cwd_key = self.request.get('current_cwd_key')
            key = ndb.Key(Directories, current_cwd_key)
            current_dir = key.get()
            stardir_key = ndb.Key(StarDirectory, user)
            stardir = stardir_key.get()

            if ((clicked_dir.subdirectory.__len__() == 0) & (clicked_dir.filenames.__len__() == 0)):
                clicked_dir_key.delete()
                del_index = current_dir.subdirectory.index(clicked_dir_ID)
                current_dir.subdirectory.remove(clicked_dir_ID)
                del current_dir.star_folder[del_index]
                current_dir.put()
                for index, each in enumerate(stardir.subdirectory):
                    if each == clicked_dir_ID:
                        del stardir.subdirectory[index]
                        del stardir.subdirectory_cwd[index]
                        stardir.put()
                        break

            else:
                message = "Error: Directory contains files/ subdirectories. Could not delete"

            for index, subdirectoryID in enumerate(current_dir.subdirectory):
                temp = ndb.Key('Directories', subdirectoryID)
                temp = temp.get()
                list_of_subdirectory.append(temp.dir_name)
                list_of_subdirectoryIDs.append(subdirectoryID)
                list_star_folder.append(current_dir.star_folder[index])

            for index, file in enumerate(current_dir.filenames):
                list_of_files.append(file)
                list_of_fileIDs.append(current_dir.blobs[index])
                list_of_filetime.append(current_dir.filetime[index])

        if action == 'Back':

            logging.info("BACK CWD:")
            logging.info("current_cwd: "+current_cwd)

            directory_key = ndb.Key(Directories, current_cwd_key)
            directory = directory_key.get()

            current_cwd_key = directory.prev_key
            current_cwd = directory.prev

            prev_cwd_key = directory.prev_key
            prev_cwd = directory.prev

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

            dir_level = dir_level-1

        if action == 'delete_file':
            print("delete file")
            deleteFile_name = self.request.get('clicked_dir')
            directory_key = ndb.Key(Directories,current_cwd_key)
            directory = directory_key.get()

            print("file to delete",deleteFile_name)
            for index, file_name in enumerate(directory.filenames):
                if deleteFile_name == file_name:
                    blobstore.delete(directory.blobs[index])
                    del directory.blobs[index]
                    del directory.filenames[index]
                    del directory.filetime[index]
                    directory.put()
                    print("deleted")
                    break

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

        if action == 'rename':
            clicked_dir_name = self.request.get('clicked_dir')
            new_name = self.request.get('new_name')
            directory_key = ndb.Key(Directories, current_cwd_key)
            directory = directory_key.get()
            exists_flag = False
            if new_name == '':
                message = "filename cannot be blank"
            else:

                for file in directory.filenames:
                    if file == new_name:
                        exists_flag = True
                        message = "File already exists"
                        break

                if exists_flag == False:
                    for index, file in enumerate(directory.filenames):
                        if file == clicked_dir_name:
                            directory.filenames[index]=new_name
                            #directory.blobs[index]
                            directory.put()
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


        if action == 'star-dir':
            print("star-dir in directoryhandler")
            clicked_dir_ID = self.request.get('clicked_dir')

            directory_key = ndb.Key(Directories, current_cwd_key)
            directory = directory_key.get()

            stardir_key = ndb.Key(StarDirectory, user)
            stardir = stardir_key.get()

            for index, subdirectoryID in enumerate(directory.subdirectory):

                if clicked_dir_ID == subdirectoryID:
                    if directory.star_folder[index]=="False":
                        directory.star_folder[index]="True"
                        directory.put()
                        stardir.subdirectory.append(directory.subdirectory[index])
                        stardir.subdirectory_cwd.append(current_cwd)
                        stardir.put()
                        break
                    if directory.star_folder[index]=="True":
                        directory.star_folder[index]="False"
                        directory.put()
                        for star_index, each in enumerate(stardir.subdirectory):
                            if subdirectoryID == each:
                                print("removing star")
                                del stardir.subdirectory[star_index]
                                del stardir.subdirectory_cwd[star_index]
                                stardir.put()
                                break

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

        #Sort by ascending order
        temp1 = []
        temp2 = []
        temp3 = []

        for x, y, z,  in sorted(zip(list_of_subdirectory, list_of_subdirectoryIDs, list_star_folder)):
            temp1.append(x)
            temp2.append(y)
            temp3.append(z)

        list_of_subdirectory = temp1
        list_of_subdirectoryIDs = temp2
        list_star_folder = temp3


        formatted_date = [datetime.datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M") for x in list_of_subdirectoryIDs ]


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
            'subdirectory_cwd': subdirectory_cwd
        }

        template = JINJA_ENVIRONMENT.get_template('display.html')
        self.response.write(template.render(template_values))
