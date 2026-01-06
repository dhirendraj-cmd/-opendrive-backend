import os
from opendrive.helpers.helper import OS_home_directory



class FolderCreations:

    def create_root_dir_per_user(self, user_id: str, parent_folder_key: str | None, display_name: str, folder_key: str):
        try:
            home_path = OS_home_directory()
            base_path = os.path.join(home_path, "data/openpidrive")
            os.makedirs(base_path, exist_ok=True)

            root_path = os.path.join(base_path, user_id, folder_key, display_name)
            print("ROOT PATH is ", root_path)

            os.makedirs(root_path, exist_ok=True)
            return root_path
        except Exception as err:
            print(f"Error is: {err}")
            return err
    

    def create_upload_dir_per_user(self, user_id: str, display_name: str, folder_key: str, parent_folder_type: str, child_folder_type: str):
        try:
            print("UPLOAD FOLDER PATH >>>>>>>>> ")
            print(user_id, folder_key, display_name, parent_folder_type, child_folder_type)

            home_path = OS_home_directory()
            base_path = os.path.join(home_path, "data/openpidrive")

            upload_path = os.path.join(base_path, user_id, folder_key, display_name)

            print("Upload path >>>> ", upload_path)

            upload_path = os.path.join(upload_path, parent_folder_type, child_folder_type)

            print("final Upload path >>>> ", upload_path)

            os.makedirs(upload_path, exist_ok=True)

            return upload_path
        except Exception as err:
            print(f"Error is: {err}")
            return err
        


        


        
        




        
