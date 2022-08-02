"""
work on Mac, delete donut images to make each patient folder contains only one donut image
"""
import os
import shutil

target = "dataset/"
folder_list = [f for f in os.listdir(target) if not f.startswith('.')]
count = 0

for folder in folder_list:
    # get file list
    file_list = [f for f in os.listdir(os.path.join(target,folder)) if not f.startswith('.')]
    for file in file_list:
        if os.path.isdir(os.path.join(target,folder,file)):
            combined_word = 0
            image_list = [f for f in os.listdir(os.path.join(target,folder,file)) if not f.startswith('.')]
            if len(image_list) > 1:
                for image in image_list:
                    if "combined" in image:
                        combined_word = 1
                if combined_word == 1:
                    for image in image_list:
                        if "combined" not in image:
                            os.remove(os.path.join(target,folder,file,image))
                            print("deleted", folder, file, image)
                            count = count + 1
                else:
                    os.remove(os.path.join(target,folder,file,image_list[1]))
                    print("deleted", folder, file, image_list[1])
                    count = count + 1
print(count, "images are deleted!")
