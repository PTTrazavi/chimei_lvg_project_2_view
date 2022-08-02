"""
work on Mac, categorize images according to the labeling result
"""
import os
import shutil
import csv

root_path = "data"
ap_folder = "AP_4_classes"
lat_folder = "Lateral_3_classes"
label_src = "data/patients_export.csv"

label_AP = {  '0': 'Normal',
              '1': 'ApicalAnterior',
              '2': 'Basal',
              '3': 'Septal',
              '4': 'deleted'
            }
label_lat = { '0': 'Normal',
              '1': 'Septal',
              '2': 'Posterolateral',
              '3': 'deleted'
            }

count_ap = 0
count_lat = 0

with open(label_src, 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    # 2:ap, 3:apl, 4:lat, 5:latl
    for row in reader:
        # AP view image
        if "no_image" not in row[2]:
            if os.path.isfile(os.path.join(root_path,row[2])):
                ap = row[2].replace("images", label_AP[row[3]])
                os.rename(os.path.join(root_path,row[2]), os.path.join(root_path,ap_folder,ap))
                count_ap = count_ap + 1
            else:
                print(row[2],"is gone!")
        # Lateral view image
        if "no_image" not in row[4]:
            if os.path.isfile(os.path.join(root_path,row[4])):
                lat = row[4].replace("images", label_lat[row[5]])
                os.rename(os.path.join(root_path,row[4]), os.path.join(root_path,lat_folder,lat))
                count_lat = count_lat + 1
            else:
                print(row[4],"is gone!")
print(count_ap, "AP view images and", count_lat, "Lateral view images")
