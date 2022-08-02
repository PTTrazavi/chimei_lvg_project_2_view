"""
work on Mac, generate csv for database and move the images to root folder
"""
import os
import shutil
import csv

target = "dataset/"
folder_list = [f for f in os.listdir(target) if not f.startswith('.')]
count = 0

csvfile = "patients.csv"
header = ['name', 'ref', 'ap', 'apl', 'lat', 'latl','date_of_update']
data = []

for folder in folder_list:
    # initialize
    row = []
    ref = "images/no_image.png"
    ap = "images/no_image.png"
    apl = 4
    lat = "images/no_image.png"
    latl = 3
    date_of_update = "-"
    # get file list
    file_list = [f for f in os.listdir(os.path.join(target,folder)) if not f.startswith('.')]
    for file in file_list:
        # find ref
        if ".jpg" in file and "-1" not in file:
            ref = "images/"+file
            os.rename(os.path.join(target,folder,file), os.path.join(target,file))
        # find ap and lat
        if os.path.isdir(os.path.join(target,folder,file)):
            if file == "AP":
                image_list = [f for f in os.listdir(os.path.join(target,folder,file)) if not f.startswith('.')]
                ap = "images/"+image_list[0]
                os.rename(os.path.join(target,folder,file,image_list[0]), os.path.join(target,image_list[0]))
            if file == "lateral":
                image_list = [f for f in os.listdir(os.path.join(target,folder,file)) if not f.startswith('.')]
                lat = "images/"+image_list[0]
                os.rename(os.path.join(target,folder,file,image_list[0]), os.path.join(target,image_list[0]))
    # generate row
    row.append(folder) # name
    row.append(ref)
    row.append(ap)
    row.append(apl)
    row.append(lat)
    row.append(latl)
    row.append(date_of_update)
    # append this row
    data.append(row)

with open(csvfile, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(data)
