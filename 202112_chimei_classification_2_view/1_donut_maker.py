from PIL import Image, ImageDraw
import os
import json
from skimage import io
import numpy as np
import cv2

target = "imagesC/"
folder_list = [f for f in os.listdir(target) if not f.startswith('.')]
if not os.path.exists("images"):
    os.mkdir("images")
if not os.path.exists("images_L"):
    os.mkdir("images_L")

# utils
def draw_combined_color(mask_image):
    colors = {0:0,      #bg 0
              1:250,    #diastole 1
              -1:100}    #systole -1

    out_image = np.zeros_like(mask_image)

    for k,v in colors.items():
        class_mask = (mask_image==k) # get the layer of class
        class_mask = class_mask * colors[k]
        out_image = out_image + class_mask

    out_image= out_image.astype(int) # make it int so plt.imshow can show rgb 0-255, float will show 0-1
    return out_image

def make_donut(folder_list, type="images", width=512, height=512, t_width=256, t_height=256):
    """
    type= "images" or "images_L"
    """
    for folder in folder_list:
        print("processing folder:", folder , "type:", type, "...")
        # set folder paths
        image_folder = os.path.join(target, folder, type)
        if "_L" in type:
            donut_name = folder + "_l.png"
        else:
            donut_name = folder + ".png"

        total_image_count = 0
        empty_json = []
        check_3 = False
        # set labels
        background = 0
        heart = 1 # 1

        # get image names
        image_list = [f for f in os.listdir(image_folder) if not f.startswith('.')]
        # print("total images:", len(image_list)/2)
        # loop through the folder
        for i in image_list:
            if i.endswith('.json'):
                # get label shape
                with open(os.path.join(image_folder,i)) as f:
                    jf = json.load(f)
                    # make sure there is shape in the dictionary
                    if len(jf['shapes']) != 0:
                        points_list = jf['shapes'][0]['points']
                        points_tuple = []
                        for p in points_list:
                            points_tuple.append(tuple(p))
                    else:
                        empty_json.append(str(i))
                        continue
                # draw a png label image
                originalImg = Image.open(os.path.join(image_folder,i.split('.')[0]+'.jpg'))
                labelImg = Image.new("L", originalImg.size, background)
                drawer = ImageDraw.Draw(labelImg)
                drawer.polygon(points_tuple, fill=heart)
                labelImg.save(os.path.join(image_folder, i.split('.')[0]+'.png')) # folder + '_' +

                total_image_count = total_image_count + 1

        # print("converted", total_image_count, "images")
        # print("empty json file:", empty_json)
        # check if you have executed this file before
        for i in image_list:
            if ".png" in i:
                check_3 = True
                break
        if check_3:
            assert len(image_list)/3 == total_image_count
        else:
            assert len(image_list)/2 == total_image_count

        if total_image_count > 1:
            # get mask names
            mask_list = [f for f in os.listdir(image_folder) if '.png' in f]
            mask_list.sort()
            mask_dict = dict(enumerate(mask_list))
            # count the pixel of heart
            heart_max = 0
            heart_min = width*height
            max_file = str()
            min_file = str()
            max_key = int()
            min_key = int()

            # get the max area image
            for k,i in enumerate(mask_list):
                mask = io.imread(os.path.join(image_folder, i)) # novel image
                # check if the size is width*height
                if mask.shape[0] != width or mask.shape[1] != height:
                    print("the size is not right!")

                # count the pixels of heart(label==1)
                heart = np.sum(mask==1)
                # find max
                if heart > heart_max:
                  heart_max = heart
                  max_file = i
                  max_key = k

            # get the min area image
            for k,i in enumerate(mask_list):
                mask = io.imread(os.path.join(image_folder, i)) # novel image
                # check if the size is width*height
                if mask.shape[0] != width or mask.shape[1] != height:
                    print("the size is not right!")

                # count the pixels of heart(label==1)
                heart = np.sum(mask==1)
                # find min
                if heart < heart_min: # and k > max_key
                  heart_min = heart
                  min_file = i
                  min_key = k

            # check the results
            # print("max_file is:", max_file)
            # print("min_file is:", min_file)

            # min image process
            mask_min = io.imread(os.path.join(image_folder, min_file))
            mask_min = mask_min * -1 # make the systole label as -1 for later calculation
            unique, counts = np.unique(mask_min, return_counts=True)
            # print("min:", dict(zip(unique, counts)))
            # max image process
            mask_max = io.imread(os.path.join(image_folder, max_file))
            unique, counts = np.unique(mask_max, return_counts=True)
            # print("max:", dict(zip(unique, counts)))
            # combine two images
            mask_combined = mask_min + mask_max
            unique, counts = np.unique(mask_combined, return_counts=True)
            # print("combined:", dict(zip(unique, counts)))
            # draw the image
            mask_combined_draw = draw_combined_color(mask_combined)
            mask_combined_draw = cv2.resize(mask_combined_draw, (t_width,t_height),
                                            interpolation=cv2.INTER_NEAREST)
            io.imsave(os.path.join(type, donut_name), mask_combined_draw)



make_donut(folder_list, type="images", width=512, height=512, t_width=256, t_height=256)
make_donut(folder_list, type="images_L", width=512, height=512, t_width=256, t_height=256)
