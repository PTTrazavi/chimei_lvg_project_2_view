import os
from skimage import io
import cv2

target = "heart_4_classes_AP_206_52/"
width, height = 256, 256

folder_list = [f for f in os.listdir(target) if not f.startswith('.')]
count = 0
count_original = 0

for folder in folder_list:
    # get image list
    image_list = [f for f in os.listdir(os.path.join(target, folder)) if not f.startswith('.')]
    count_original += len(image_list)

    for image in image_list:
        img = io.imread(os.path.join(target, folder, image))
        # resize to width*height
        img = cv2.resize(img, (width,height), interpolation=cv2.INTER_NEAREST)
        # save the resized image
        io.imsave(os.path.join(target, folder, image), img)
        count += 1

print("resized", count, "images from", count_original, "images!")
