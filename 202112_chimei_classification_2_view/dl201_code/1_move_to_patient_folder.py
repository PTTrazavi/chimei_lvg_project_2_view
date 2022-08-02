"""
work on Mac, copy donuts to the related patient folder
"""
import os
import shutil

target = "dataset/"
source = "heart_3_classes_L_152_38/"
work = "lateral"

target_list = [f for f in os.listdir(target) if not f.startswith('.')]
source_list = [f for f in os.listdir(source) if not f.startswith('.')]

for s_folder in source_list:
    # get image list
    image_list = [f for f in os.listdir(os.path.join(source,s_folder)) if not f.startswith('.')]
    for image in image_list:
        check_name = image.split(" ")[0]
        check_name = check_name.split("_")[0]
        for t_folder in target_list:
            if check_name in t_folder:
                if not os.path.exists(os.path.join(target,t_folder,work)):
                    os.mkdir(os.path.join(target,t_folder,work))
                shutil.copyfile(os.path.join(source,s_folder,image), os.path.join(target,t_folder,work,image))
