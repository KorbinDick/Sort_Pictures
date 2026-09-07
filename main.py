##########################################################################################################################################################
# Video/Image Sorter
# 
# 
# Given a path of a folder that holds disorganzied pictures/videos, this script will scan all content of the directory and subdirectories, extract
# the creation data of each piece of media, and then create folders based on the data etxracted, grouped by month and year
#
#
#
#
##########################################################################################################################################################


from pathlib import Path
from PIL import Image
import datetime

folder_path = Path(r"E:\OBX_2026\100D5000")

def get_video_date(file_path):
    try:
        return datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
    except Exception:
        return None















if folder_path.exists() and folder_path.is_dir():
    print(f"Scanning folder and subfolders: {folder_path}\n")
    
    for file_path in folder_path.rglob("*"):
        if not file_path.is_file():
            continue
            
        ext = file_path.suffix.lower()
        
        if ext in (".jpg", ".jpeg", ".png"):
            print(f"[IMAGE] {file_path.relative_to(folder_path)}")
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
            print(f"[VIDEO] {file_path.relative_to(folder_path)}")
            date_taken = get_video_date(file_path)
            print(f"   -> Date Taken: {date_taken or 'No metadata date found'}")
            print("-" * 50)
else:
    print("The specified path does not exist or is not a directory.")
