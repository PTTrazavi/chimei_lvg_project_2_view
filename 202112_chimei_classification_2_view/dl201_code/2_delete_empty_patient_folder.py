"""
work on Mac, delete patient folder without any donut image
"""
import os
import shutil

target = "dataset/"

folder_list = [f for f in os.listdir(target) if not f.startswith('.')]


for folder in folder_list:
    # get file list
    file_list = [f for f in os.listdir(os.path.join(target,folder)) if not f.startswith('.')]
    check = 0
    for file in file_list:
        if os.path.isdir(os.path.join(target,folder,file)):
            # print("found folder", file)
            check = 1
    if check == 0:
        shutil.rmtree(os.path.join(target,folder))
        print("delete folder", folder)
