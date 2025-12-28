import os
import shutil
import secrets
from opendrive.uploaders.file_models import Folder
from opendrive.helpers.helper import OS_home_directory



class FolderCreations:

    home_path = OS_home_directory()
    base_path = "data/openpidrive/"

    BASE_FOLDER_PATH = os.path.join(home_path, base_path)

    def create_directories_per_user(self, user_id: str):
        real_folder_path = FolderCreations.BASE_FOLDER_PATH + "user_" + user_id
        print("real_folder_path>>>>>>>>>>>>>>>>>> ", real_folder_path)

        if not os.path.exists(real_folder_path):
            folder_key_path = real_folder_path + "/" + "fo_" + secrets.token_urlsafe(8)
            real_folder_path = os.path.join(real_folder_path, folder_key_path)
            real_folder_path = os.makedirs(real_folder_path, exist_ok=True)
            print("real path is >>>>>>>> ", real_folder_path)
        else:
            print("User folder already exists>>>>>>>>>>>>>>>>>>>>>")
        return real_folder_path
        




        
