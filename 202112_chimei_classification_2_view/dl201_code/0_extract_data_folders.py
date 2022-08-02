"""
work in 201, copy patient folder to "result" folder 
"""
import os

target = "/mnt/data/jeremy/chimei/20210608/"
result = "dataset/"

folder_list = [f for f in os.listdir(target) if not f.startswith('.')]

for folder in folder_list:
    # make local folder without space
    folder_nos = folder.replace(" ", "_")
    folder_nos = folder_nos.replace("(", "_")
    folder_nos = folder_nos.replace(")", "_")

    # generate name with escape \ for source folder
    folder_src = folder.replace(" ", "\ ")
    folder_src = folder_src.replace("(", "\(")
    folder_src = folder_src.replace(")", "\)")
    print(folder)
    # make local folder
    os.mkdir(result+folder_nos)
    # get file list
    file_list = [f for f in os.listdir(os.path.join(target, folder)) if not f.startswith('.')]

    for file in file_list:
        if ".jpg" in file:
            # generate name with escape \ for source file
            file_src = file.replace(" ", "\ ")
            file_src = file_src.replace("(", "\(")
            file_src = file_src.replace(")", "\)")
            os.system("cp "+target+folder_src+"/"+file_src+" "+result+folder_nos+"/"+file_src)
