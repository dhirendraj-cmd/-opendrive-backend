import os
from opendrive.helpers.helper import OS_home_directory



class FolderCreations:

    def create_root_dir_per_user(self, user_id: str, parent_folder_key: str | None, display_name: str, folder_key: str):
        home_path = OS_home_directory()
        base_path = os.path.join(home_path, "data/openpidrive")
        os.makedirs(base_path, exist_ok=True)

        root_path = os.path.join(base_path, user_id, folder_key, display_name)
        print("ROOT PATH is ", root_path)

        os.makedirs(root_path, exist_ok=True)
        return root_path
    

    def create_upload_dir_per_user(self, user_id: str, parent_folder_key: str | None, display_name: str, folder_key: str):
        pass


        


        
        




        
