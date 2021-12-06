import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
import csv_to_shp
import shp_to_dxf
import tif_to_csv

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    # gather file information
    file_path = f"{event.src_path}"
    last_slash = file_path.rfind("/")
    file_name = file_path[last_slash + 1:]
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M")
    # delete all files in konvertert mappe
    if ".csv" in file_path or ".shp" in file_path or ".tif" in file_path:
        time.sleep(5)
        for file in os.listdir(f"{folder}/02_konvertert"):
            os.remove(f"{folder}/02_konvertert/{file}")
            with open(f"{folder}/04_script/log.txt", "a") as f:
                f.write(f"{timestamp}: deleted {file} in 02_konvertert\n")
    # pass file information to appropriate script
    if ".csv" in file_path:
        with open(f"{folder}/04_script/log.txt", "a") as f:
            f.write(f"{timestamp}: {file_name} detected, conversion started\n")
        print(f"csv detected: {file_name}")
        csv_to_shp.main(file_path=file_path, file_name=file_name, timestamp=timestamp)
        time.sleep(2)
        os.rename(file_path, dst=f"{folder}/03_arkiv/csv_to_shp/{timestamp}_{file_name}")
    elif ".shp" in file_path:
        with open(f"{folder}/04_script/log.txt", "a") as f:
            f.write(f"{timestamp}: {file_name} detected, conversion started\n")
        file_path_dbf = f"{file_path[:-4]}.dbf"
        file_path_prj = f"{file_path[:-4]}.prj"
        file_path_shx = f"{file_path[:-4]}.shx"
        print(f"shp detected: {file_name}")
        time.sleep(3)
        shp_to_dxf.main(file_path, file_name, timestamp)
        time.sleep(2)
        os.rename(file_path, dst=f"{folder}/03_arkiv/shp_to_dxf/{timestamp}_{file_name}")
        os.rename(file_path_dbf, dst=f"{folder}/03_arkiv/shp_to_dxf/{timestamp}_{file_name[:-4]}.dbf")
        os.rename(file_path_prj, dst=f"{folder}/03_arkiv/shp_to_dxf/{timestamp}_{file_name[:-4]}.prj")
        os.rename(file_path_shx, dst=f"{folder}/03_arkiv/shp_to_dxf/{timestamp}_{file_name[:-4]}.shx")
    elif ".tif" in file_path:
        print("writing to log...")
        with open(f"{folder}/04_script/log.txt", "a") as f:
            f.write(f"{timestamp}: {file_name} detected, beginning conversion\n")
        print(f"tif detected: {file_name}")
        tif_to_csv.main(file_path, file_name, timestamp)
        time.sleep(2)
        print("moving file...")
        os.rename(file_path, dst=f"{folder}/03_arkiv/tif_to_csv/{timestamp}_{file_name}")

    else:
        pass
    # delete file three seconds after scripts have been run
    # time.sleep(3)
    # os.remove(file_path)


def on_deleted(event):
    pass

def on_modified(event):
    pass

def on_moved(event):
    pass

# specify absolute filepath for konvertering folder
folder = "/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering"

# startup message
print("script started...")
my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = f"{folder}/01_inn"
go_recursively = False  # changed to False
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
