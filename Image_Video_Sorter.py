##########################################################################################################################################################
#                                                                   Video/Image Sorter
# 
# 
#   Given a path of a folder that holds disorganzied pictures/videos, this script will scan all content of the directory and subdirectories, extract
#   the creation data of each piece of media, and then create folders based on the data etxracted, grouped by month and year
#
#   Possible future implementation is to create another new folder to put all non-avi/jpg/jpeg/png/mp4/mov files into
#
#
#
#
##########################################################################################################################################################


##########################################################################################################################################################
#                                                              Explanation of imports/modules:
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
##########################################################################################################################################################

from pathlib import Path
from PIL import Image
import datetime
import sys
import shutil
import keyboard
import os


#holds the original path for the folder to be organized
input_folder_path = Path(r"E:\Drives")
output_folder_path = Path(r"D:\Drives_Organized")
# input_folder_path = Path(r"E:\OBX_2026")
# output_folder_path = Path(r"D:\Drives_Organized")

oldest_folder_year = 2000
newest_folder_year = 2026

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

non_image_folder = output_folder_path / "non_image"

log_folder = output_folder_path / "log"

exit_keys = ['esc']

# functions
def confirm_action(prompt):
    valid_responses = {"yes": True, "y": True, "no": False, "n": False}
    prompt_suffix = " [Y/n]: "

    while True:
        user_input = input(prompt + prompt_suffix).strip().lower()
        if user_input == "":
            return True
        if user_input in valid_responses:
            return valid_responses[user_input]
        print("Invalid input. Please enter 'y' or 'n'")

def user_interrupt(key):
    if key == keyboard.Key.esc:
        print("\nUSER EXIT, SCRIPT HAS BEEN ABORTED.")
        os._exit(0) 


# main script execution
if input_folder_path.exists() and input_folder_path.is_dir():

    if confirm_action(f"Do you want to create/copy content to path {output_folder_path}?"):
        print("poo")
        output_folder_path.mkdir(parents=True, exist_ok=True)
        for i in range(newest_folder_year - oldest_folder_year + 1):
            year = oldest_folder_year + i
            for month in months:
                month_folder_path = output_folder_path / str(year) / str(month)
                month_folder_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {month_folder_path}") 
        non_image_folder.mkdir(parents=True, exist_ok=True)
        log_folder.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Script has been aborted and will not create folders or copy content to path {output_folder_path}")
        sys.exit(1)


    print(f"\nScanning folder and subfolders: {input_folder_path}\n")




    for file_path in input_folder_path.rglob("*"):
        if not file_path.is_file():
            continue


        if any(keyboard.is_pressed(key) for key in exit_keys):
            print("\nUSER EXIT. SCRIPT ABORTED. POO.")
            sys.exit(0)
        try:
                        
            ext = file_path.suffix.lower()
                    
            if ext in (".jpg", ".jpeg", ".png", ".cr2"):
                print(f"[IMAGE] {file_path.relative_to(input_folder_path)}")
                with Image.open(file_path) as img:
                    date_taken = None
                                
                    if ext in (".jpg", ".jpeg", ".cr2"):
                        exif_data = img._getexif()
                        date_taken = exif_data.get(36867) if exif_data else None
                                
                    elif ext == ".png":
                        info = img.info
                        date_taken = info.get("Creation Time") or info.get("date:create")
                                    
                                
                    print(f"Date Taken: {date_taken}")
                    image_year = date_taken.split(":")[0]
                    image_month = date_taken.split(":")[1]
                    base_path = output_folder_path / image_year / list(months.keys())[int(image_month)-1]
                    name_suffix = f"{file_path.stem}{file_path.suffix}"
                    goal_path = base_path / name_suffix
                    copies = 1
                    while goal_path.exists():
                        copy_add = f"_copy{copies}"
                        goal_path = base_path / f"{file_path.stem}{copy_add}{file_path.suffix}"
                        copies += 1
                    print(f"Copying file to: {goal_path}\n")
                    shutil.copy(file_path, goal_path)
                        
            elif ext in (".mov", ".mp4", ".avi", ".mts"):
                print(f"[VIDEO] {file_path.relative_to(input_folder_path)}")
                date_taken = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                print(f"Date Taken: {date_taken}")
                video_year = date_taken.strftime("%Y")
                video_month = date_taken.strftime("%m")
                base_path = output_folder_path / video_year / list(months.keys())[int(video_month)-1]
                name_suffix = f"{file_path.stem}{file_path.suffix}"
                goal_path = base_path / name_suffix
                copies = 1
                while goal_path.exists():
                    copy_add = f"_copy{copies}"
                    goal_path = base_path / f"{file_path.stem}{copy_add}{file_path.suffix}"
                    copies += 1
                print(f"Copying file to: {goal_path}\n")
                shutil.copy(file_path, goal_path)
                        
            
            else:
                print(f"[OTHER] {file_path.relative_to(input_folder_path)}")
                name_suffix = f"{file_path.stem}{file_path.suffix}"
                goal_path = non_image_folder / name_suffix
                copies = 1
                while goal_path.exists():
                    copy_add = f"_copy{copies}"
                    goal_path = non_image_folder / f"{file_path.stem}{copy_add}{file_path.suffix}"
                    copies += 1
                print(f"Copying file to: {goal_path}\n")
                shutil.copy(file_path, goal_path)
            
        except Exception:
            print(f"Content that failed to be sorted: {file_path}")
            shutil.copy(file_path, log_folder / f"{file_path.stem}{file_path.suffix}")

        
    print("*" * 150)
    print("SORTING HAS BEEN COMPLETED. SEE DESTINATION FOLDER FOR RESULTS AND LOG FOLDER FOR POTENTIAL ERRORS.")
    print("*" * 150)

else:
    print(f"CHECK INPUT PATH. IT DOES NOT EXIST OR IS NOT A DIRECTORY. ERROR IN {input_folder_path}")
    sys.exit(1)
