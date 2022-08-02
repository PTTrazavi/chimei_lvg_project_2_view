"""
Delete images without json label files
"""
from PIL import Image
import os

# get folder names
image_folder = "imagesC/"
image_folder_list = [f for f in os.listdir(image_folder) if not f.startswith('.')]
print("total image folders:", len(image_folder_list))
print("first 3 folders:", image_folder_list[:3])

# loop through each folder and delete jpg without json
for folder in image_folder_list:
    image_list = [i for i in os.listdir(os.path.join(image_folder, folder, "images")) if not i.startswith('.')]
    count = 0
    for i in image_list:
        if i.endswith('.jpg') and (i.split('.')[0]+'.json') not in image_list:
            os.remove(os.path.join(image_folder, folder, "images", i))
            count = count + 1
    print("deleted", count, "images in folder", folder, "/images/")

    image_list = [i for i in os.listdir(os.path.join(image_folder, folder, "images_L")) if not i.startswith('.')]
    count = 0
    for i in image_list:
        if i.endswith('.jpg') and (i.split('.')[0]+'.json') not in image_list:
            os.remove(os.path.join(image_folder, folder, "images_L", i))
            count = count + 1
    print("deleted", count, "images in folder", folder, "/images_L/")
