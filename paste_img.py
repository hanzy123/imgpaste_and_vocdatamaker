# coding: utf-8
# this file to make paste-logo images
# author hanzy 2016_11_10

from PIL import Image 
import random
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("img_savepath",
    help = "where u want to save your paste_images,example:/Users/mac/logo_detection/paste_img/new_img")
parser.add_argument("logo_dir",
    help = "where u saving your logo_examples,example:/Users/mac/logo_detection/paste_img/0_logo_dataset")
parser.add_argument("bg_dir",
    help = "where u saving your bg_images: example:/Users/mac/logo_detection/dataset/FlickrLogos-32/classes/jpg/no-logo")
parser.add_argument("img_info_for_XML",
    help = "where u want to save your position_info.txt,example:/Users/mac/logo_detection/paste_img/position_info.txt")
args = parser.parse_args()

# img_savepath = '/Users/mac/logo_detection/paste_img/new_img'
img_savepath = args.img_savepath

# logo_dir = '/Users/mac/logo_detection/paste_img/0_logo_dataset'
logo_dir = args.logo_dir

# bg_dir = '/Users/mac/logo_detection/dataset/FlickrLogos-32/classes/jpg/no-logo'
bg_dir = args.bg_dir

# img_info_for_XML = '/Users/mac/logo_detection/paste_img/position_info.txt'
img_info_for_XML = args.img_info_for_XML

bg_file_paths = []
logo_dir_paths = []
logo_paths = []
position_info = []

def getlogo_type_dir_path(args, dirname, filenames):
    """
    Callback Function

    @params:
    args : the parameter of os.path.walk(logo_dir, getlogo_type_dir_path, None)
    dirname : folder locations
    filename : filename in folder locations
    """

    for filename in filenames:
        if os.path.isdir(dirname + '/' + filename):
            logo_dir_paths.append(dirname + '/' + filename)


def getbg_path(args, dirname, filenames):
    """
    Callback Function

    @params:
    args : the parameter of os.path.walk(bg_dir, getbg_path, None)
    dirname : folder locations
    filename : filename in folder locations
    """

    for filename in filenames:
        if filename[-3:] == 'jpg':
            bg_file_paths.append(dirname + '/' + filename)


def getlogo_path (args, dirname, filenames):
    """
    Callback Function

    @params:
    args : the parameter of os.path.walk(logo_dir_path, getlogo_path, None)
    dirname : folder locations
    filename : filename in folder locations
    """

    for filename in filenames:
        if os.path.isfile(dirname + '/' + filename):
            logo_paths.append(dirname + '/' + filename)  


def writepathtotxt(data_sets):
    """

    @params:
    data_sets : the information lists
    """

    # use to save data_set infos
    txt_path = img_info_for_XML

    with open(txt_path,"w") as f:
        for data_set in data_sets:
            f.write(data_set)
            f.write('\n')


#get bg img path
os.path.walk(bg_dir, getbg_path, None)

#get logo dir path
os.path.walk(logo_dir, getlogo_type_dir_path, None)

#do
for logo_dir_path in logo_dir_paths:
    count = 0
    logo_paths = []
    
    #get one-type-logo's paths save in logo_paths
    os.path.walk(logo_dir_path, getlogo_path, None)
    while(1):
        logo_id = random.randint(0, np.size(logo_paths)-1)
        bg_file_id = random.randint(0, np.size(bg_file_paths)-1)
        try:
            #read img
            imglogo = Image.open(logo_paths[logo_id])
            imgbg = Image.open(bg_file_paths[bg_file_id])

            #get logo img size && background img size
            logo_length,logo_weigh = imglogo.size
            bg_length,bg_weigh = imgbg.size

            if(bg_length > bg_weigh):
                my_length = bg_weigh
            else:
                my_length = bg_length
                
            #get logo img resize size by random in (1/16,1/2)
            while(1):
                target_length = random.randint(my_length/16, my_length/2)
                target_weigh = logo_weigh * target_length / logo_length
                if target_length < bg_length and target_weigh < bg_weigh:
                    break;

            #resize logo img
            mylogo = imglogo.resize((target_length, target_weigh), Image.ANTIALIAS)

            #which bg position target paste to 
            point_position_x = random.randint(0, bg_length - target_length)
            point_position_y = random.randint(0, bg_weigh - target_weigh)

            #paste logo
            box = (point_position_x,point_position_y,point_position_x + target_length,point_position_y + target_weigh)
            imgbg.paste(mylogo, box)
            imgbg.save(img_savepath + '/' + logo_dir_path.split('/')[-1] + '_' + str(count) + '.jpg')
            count += 1

            positioninfo = [logo_dir_path.split('/')[-1],'_',str(count),' ',logo_dir_path.split('/')[-1],' ',
                str(point_position_x),' ',str(point_position_y),' ',str(point_position_x + target_length),' ',
                str(point_position_y + target_weigh)]
            position_info.append(''.join(positioninfo))
            
            #every type of logo make 500 pages
            if count > 500:
                print 'logo  ' + logo_dir_path.split('/')[-1] + '  finish!'
                break
        except:
            continue

#save out position_info
writepathtotxt(position_info)

print 'Done!'
