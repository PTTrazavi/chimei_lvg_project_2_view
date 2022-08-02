"""
work on Mac, check each patient folder
"""
import os
import shutil

target = "dataset/"
folder_list = [f for f in os.listdir(target) if not f.startswith('.')]
count = 0
count_0 = 0
count_3 = 0

for folder in folder_list:
    # get file list
    file_list = [f for f in os.listdir(os.path.join(target,folder)) if not f.startswith('.')]
    for file in file_list:
        if os.path.isdir(os.path.join(target,folder,file)):
            image_list = [f for f in os.listdir(os.path.join(target,folder,file)) if not f.startswith('.')]
            if len(image_list) > 1:
                print(folder,file)
                count = count + 1
            elif len(image_list) == 0:
                print(folder,"contains 0 image!!!!!!!!!!")
                count_0 = count_0 + 1
            if len(image_list) == 3:
                print(folder,"contains 3 image!!!!!!!!!!")
                count_3 = count_3 + 1

print(count, "folders contain more than 1 image!")
print(count_0, "folders contain 0 image!")
print(count_3, "folders contain 3 images!")
