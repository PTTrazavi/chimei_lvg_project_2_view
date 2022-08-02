"""
combine front view and lateral view images, resize to target size
front view images are in "images" folder, lateral view images are in "images_L" folder
"""
from PIL import Image, ImageDraw
import os
import json
from shutil import copyfile, rmtree
import numpy as np
import cv2

total_image_count = 0
empty_json = []

# set labels and size
background = 0
heart = 1 # 1
width = 256*2
height = 256

# set folder paths
train_folder = "to_Azure/chimei_2v_t_v/train/"
train_label_folder = "to_Azure/chimei_2v_t_v/trainannot/"
image_root = "imagesC/"

temp_images = "temp_images"
temp_images_mask = "temp_images_mask"
temp_images_L = "temp_images_L"
temp_images_L_mask = "temp_images_L_mask"

# get folder names
image_root_list = [f for f in os.listdir(image_root) if not f.startswith('.')]
print("total image folders:", len(image_root_list))

# loop through each folder
for folder in image_root_list:
    # make temp folders
    if not os.path.exists(temp_images):
        os.mkdir(temp_images)
    if not os.path.exists(temp_images_mask):
        os.mkdir(temp_images_mask)
    if not os.path.exists(temp_images_L):
        os.mkdir(temp_images_L)
    if not os.path.exists(temp_images_L_mask):
        os.mkdir(temp_images_L_mask)

    # loop through front view folder
    image_folder = os.path.join(image_root, folder, "images")
    # don't include hidden file in mac
    image_list = [f for f in os.listdir(image_folder) if not f.startswith('.')]
    print("total images in", folder, "/images/:", len(image_list)/2)
    # loop through each image
    for i in image_list:
        if i.endswith('.json'):
            # get label shape
            with open(os.path.join(image_folder,i)) as f:
                jf = json.load(f)
                # print("generating",folder,i)
                # make sure there is shape in the dictionary
                if len(jf['shapes']) != 0:
                    points_list = jf['shapes'][0]['points']
                    points_tuple = []
                    for p in points_list:
                        points_tuple.append(tuple(p))
                else:
                    empty_json.append(str(image_folder + '/' + i))
                    continue
            # draw a png label image
            originalImg = Image.open(os.path.join(image_folder,i.split('.')[0]+'.jpg'))
            labelImg = Image.new("L", originalImg.size, background)
            drawer = ImageDraw.Draw(labelImg)
            drawer.polygon(points_tuple, fill=heart)
            labelImg.save(os.path.join(temp_images_mask,folder + '_' + i.split('.')[0]+'.png'))
            # copy the original image to training folder
            copyfile(os.path.join(image_folder,i.split('.')[0]+'.jpg'),
                    os.path.join(temp_images,folder + '_' + i.split('.')[0]+'.png'))

    # loop through lateral view folder
    image_folder = os.path.join(image_root, folder, "images_L")
    # don't include hidden file in mac
    image_list = [f for f in os.listdir(image_folder) if not f.startswith('.')]
    print("total images in", folder, "/images_L/:", len(image_list)/2)
    # loop through each image
    for i in image_list:
        if i.endswith('.json'):
            # get label shape
            with open(os.path.join(image_folder,i)) as f:
                jf = json.load(f)
                # print("generating",folder,i)
                # make sure there is shape in the dictionary
                if len(jf['shapes']) != 0:
                    points_list = jf['shapes'][0]['points']
                    points_tuple = []
                    for p in points_list:
                        points_tuple.append(tuple(p))
                else:
                    empty_json.append(str(image_folder + '/' + i))
                    continue
            # draw a png label image
            originalImg = Image.open(os.path.join(image_folder,i.split('.')[0]+'.jpg'))
            labelImg = Image.new("L", originalImg.size, background)
            drawer = ImageDraw.Draw(labelImg)
            drawer.polygon(points_tuple, fill=heart)
            labelImg.save(os.path.join(temp_images_L_mask,folder + '_' + i.split('.')[0]+'.png'))
            # copy the original image to training folder
            copyfile(os.path.join(image_folder,i.split('.')[0]+'.jpg'),
                    os.path.join(temp_images_L,folder + '_' + i.split('.')[0]+'.png'))

    # combine 2 view images and resize it to target size
    temp_image_list = [f for f in os.listdir(temp_images) if not f.startswith('.')]
    temp_image_L_list = [f for f in os.listdir(temp_images_L) if not f.startswith('.')]
    assert len(temp_image_list) == len(temp_image_L_list)
    print("combining", len(temp_image_list), "images")
    for i in range(len(temp_image_list)):
        # generate image
        img = cv2.imread(os.path.join(temp_images, temp_image_list[i]))
        img_L = cv2.imread(os.path.join(temp_images_L, temp_image_L_list[i]))
        vis = np.concatenate((img, img_L), axis=1)
        vis = cv2.resize(vis, (width,height), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(os.path.join(train_folder, temp_image_list[i].split('.')[0]+temp_image_L_list[i].split('.')[0].split('_')[-1]+'.png'), vis)
        # generate mask
        img = cv2.imread(os.path.join(temp_images_mask, temp_image_list[i]))
        img_L = cv2.imread(os.path.join(temp_images_L_mask, temp_image_L_list[i]))
        vis = np.concatenate((img, img_L), axis=1)
        vis = cv2.resize(vis, (width,height), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(os.path.join(train_label_folder, temp_image_list[i].split('.')[0]+temp_image_L_list[i].split('.')[0].split('_')[-1]+'.png'), vis)
        # counter
        total_image_count = total_image_count + 1

    # delete temp folders
    rmtree(temp_images)
    rmtree(temp_images_mask)
    rmtree(temp_images_L)
    rmtree(temp_images_L_mask)

print("converted", total_image_count, "images")
print("empty json file:", empty_json)
