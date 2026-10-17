import os
import zipfile
from datetime import datetime

def run_automated_user_backup(save_destination):
    # 1. dynamically find the cative windows user profile path
    
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        print("Error: could not determine the windows user profile.")
        return

    # 2. define the self high exact folder you want to backup
    # This capture documens, desktop items, and source repositories cleanly
    
    target_folders = ["Documents", "Desktop", "Source", "Projects"]

    # 3. Explicity define system paths to ignore to prevent permission crashes and bloat

    ignore_list = ["AppData", "Local Settings", "Application Data", "OneDrive", "Temp", ".Virtualbox"]

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"{current_time}_Full_User_Profile_Backup.zip"
    full_output_path = os.path.join(save_destination, zip_filename)

    if not os.path.exists(save_destination):
        os.makedirs(save_destination)

    print(f"Initializin safe automated backup for profile: {user_profile}")

    try:
        with zipfile.ZipFile(full_output_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
            # loop through each target folder
            
            for folder in target_folders:
                folder_path = os.path.join(user_profile, folder)

                if not os.path.exists(folder_path):
                    continue # safely skip if folder doesnt exist on this specific machine

                print(f"Archiving folder path: {folder_path}...")

                for root, dirs, files in os.walk(folder_path):
                    # Bypassing ignore dirctories automatically to prevent crashes
                    dirs[:] = [d for d in dirs if d not in ignore_list and not d.startswith('.')]

                    for file in files:
                        # Skip hidden lock files and temporary files automatically
                        
                        if file.startswith('~$') or file.endswith('.tmp') or file == 'ntuser.dat':
                            continue

                        full_file_path = os.path.join(root, file)
                        try:
                            # Generate a structure relative path inside the zip file archive

                            relative_path = os.path.relpath(full_file_path, user_profile)
                            zipf.write(full_file_path, relative_path)
                        except (PermissionError, FileNotFoundError):
                            # Safely log and skip any file actively locked y onother open program

                            print(f"skipping locked file: {file}")
                            continue
            print("\nSucces! All available folders archived cleanly to:\n --> {full_output_path}")
    except Exception as e:
        print(f"An unexcepted critical error occured during execution: {e}")

if __name__ == "__main__":
    # specify where to drop the complete zip archive

    ARCHIVE_DIRECTORY = "c:\\BackupsArchive"
    run_automated_user_backup(ARCHIVE_DIRECTORY)