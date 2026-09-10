##########################################################################################################################################################
# Video/Image Sorter
# 
# 
# Given a path of a folder that holds disorganzied pictures/videos, this script will scan all content of the directory and subdirectories, extract
# the creation data of each piece of media, and then create folders based on the data etxracted, grouped by month and year

# Possible future implementation is to create another new folder to put all non-avi/jpg/jpeg/png/mp4/mov files into
#
#
#
#
##########################################################################################################################################################


####################################################################################################
# Explanation of imports/modules:
# pathlib -> represents paths as objects, instead of strings like usually done in other modules
# reference: https://docs.python.org/3/library/pathlib.html

# PIL -> for image processing, inspecting metadata on .jpg/jpeg/png files
# reference: https://pillow.readthedocs.io/en/stable/

# datetime -> for working with dates and times, formatting, and extracting date information from files
# reference: https://docs.python.org/3/library/datetime.html

# platform -> for getting information about the operating system
# reference :
#
# Other references:
# https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
#
#
#
####################################################################################################
from pathlib import Path
from PIL import Image
import datetime
import platform
import sys
 #from statx import statx

#holds the original path for the folder to be organized
input_folder_path = Path(r"E:\OBX_2026\100D5000")
output_folder_path = Path(r"C:\Users\Korbi\Desktop\OBX_2026_Organized")

oldest_folder_year = 2000
newest_folder_year = 2026






# functions
def get_video_date(file_path):
    if platform.system() == "Windows":
        try:
            return datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
        except Exception:
            return None
    elif platform.system() == "Linux":
        try:
            return datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
        except Exception:
            return None


def confirm_action(prompt="Do you want to continue?", default=True):
    valid_responses = {"yes": True, "y": True, "no": False, "n": False}
    
    if default is True:
        prompt_suffix = " [Y/n]: "
    elif default is False:
        prompt_suffix = " [y/N]: "
    else:
        prompt_suffix = " [y/n]: "

    while True:
        user_input = input(prompt + prompt_suffix).strip().lower()
        
        if user_input == "" and default is not None:
            return default
            
        if user_input in valid_responses:
            return valid_responses[user_input]
            
        print("Invalid input. Please enter 'y' or 'n'.")







# main script execution
if confirm_action(f"Do you want to create/overwrite content at folder path {output_folder_path}?"):
    for i in range(newest_folder_year - oldest_folder_year + 1):
        print("poo")
        # folder_name = f""
        # folder_path = output_folder_path / folder_name
        # folder_path.mkdir(parents=True, exist_ok=True)
else:
    print(f"Script has been aborted and will not create/overwrite folders/file content at {output_folder_path}")
    sys.exit(1)





if input_folder_path.exists() and input_folder_path.is_dir():
    print(f"Scanning folder and subfolders: {input_folder_path}\n")
    
    for file_path in input_folder_path.rglob("*"):
        if not file_path.is_file():
            continue
            
        ext = file_path.suffix.lower()
        
        if ext in (".jpg", ".jpeg", ".png"):
            print(f"[IMAGE] {file_path.relative_to(input_folder_path)}")
            try:
                with Image.open(file_path) as img:
                    date_taken = None
                    
                    if ext in (".jpg", ".jpeg"):
                        exif_data = img._getexif()
                        date_taken = exif_data.get(36867) if exif_data else None
                    
                    elif ext == ".png":
                        info = img.info
                        date_taken = info.get("Creation Time") or info.get("date:create")
                        
                    print(f"   -> Date Taken: {date_taken or 'No embedded date found'}")
            except Exception as e:
                print(f"   -> Error reading image metadata: {e}")
            print("-" * 50)
            
        elif ext in (".mov", ".mp4", ".avi"):
            print(f"[VIDEO] {file_path.relative_to(input_folder_path)}")
            date_taken = get_video_date(file_path)
            print(f"   -> Date Taken: {date_taken or 'No metadata date found'}")
            print("-" * 50)
else:
    print("The specified path does not exist or is not a directory.")
