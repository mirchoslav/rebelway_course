import hou
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import sys

PATH_TO_OAUTH_FILE = r"C:\Miro\Python\Repo\rebelway_course\client_secrets.json"

class UploadToGDrive:
    @staticmethod
    def create_cache_file():
        input_node = hou.pwd().input(0)
        if not input_node:
            print("Input is empty!")
            return None
        
        cache_file = f"$HIP/{input_node.name()}.abc"
        
        cache_node = input_node.createOutputNode("filecache::2.0")
        cache_node.parm("filemethod").set(1)
        cache_node.parm("trange").set(0)
        cache_node.parm("file").set(cache_file)
        cache_node.parm("execute").pressButton()
        
        cache_file_expanded = cache_node.parm("file").evalAsString()
        
        cache_node.destroy()
        return cache_file_expanded
        
    @staticmethod
    def uplod_to_gdrive(upload_file):
        drive_login = GoogleAuth()
        drive_login.DEFAULT_SETTINGS['client_config_file'] = PATH_TO_OAUTH_FILE
        drive_login.LocalWebserverAuth()
        gdrive = GoogleDrive(drive_login)
        
        id_folder = "1YsdrsUT1IqhJUUwYdqE1HkQKL-Qttwa9"
        metadata = {
            "parents": [
                {"id": id_folder}
            ],
            "title" : os.path.basename(upload_file)
        }        
        drive_file = gdrive.CreateFile(metadata=metadata)
        drive_file.SetContentFile(upload_file)
        drive_file.Upload()
        

def execute()           
    cache_file = UploadToGDrive.create_cache_file()
    if cache_file and os.path.exists(cache_file):
        UploadToGDrive.uplod_to_gdrive(cache_file)
    else:
        print("No cache file!")