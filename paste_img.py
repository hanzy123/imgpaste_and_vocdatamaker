# coding: utf-8
# this file to make paste-logo images
# author hanzy 2016_11_10

import cv2
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
parser.add_argument("lower_bound",
    help = "which Image size Lower bound u want to set,example:0.2",type = float)
parser.add_argument("up_bound",
    help = "which Image size up bound u want to set,example:0.5",type = float)
parser.add_argument("picture_count_per_logo",
    help = "How many pictures per logo u want to make ,example:100",type = int)
args = parser.parse_args()

# img_savepath = '/Users/mac/logo_detection/paste_img/new_img'
img_savepath = args.img_savepath

# logo_dir = '/Users/mac/logo_detection/paste_img/0_logo_dataset'
logo_dir = args.logo_dir

# bg_dir = '/Users/mac/logo_detection/dataset/FlickrLogos-32/classes/jpg/no-logo'
bg_dir = args.bg_dir

# img_info_for_XML = '/Users/mac/logo_detection/paste_img/position_info.txt'
img_info_for_XML = args.img_info_for_XML

lower_bound = args.lower_bound

up_bound = args.up_bound

picture_count_per_logo = args.picture_count_per_logo

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
            imglogo = cv2.imread(logo_paths[logo_id], cv2.CV_LOAD_IMAGE_UNCHANGED)
            imgbg = cv2.imread(bg_file_paths[bg_file_id], cv2.CV_LOAD_IMAGE_UNCHANGED)
        
            #get logo img size && background img size
            logo_length = imglogo.shape[1]
            logo_weigh = imglogo.shape[0]
            bg_length = imgbg.shape[1]
            bg_weigh = imgbg.shape[0]

            if(bg_length > bg_weigh):
                my_length = bg_weigh
            else:
                my_length = bg_length
                #get logo img resize size by random in (1/16,1/2)
            while(1):
                target_length = random.randint(int(my_length*lower_bound), int(my_length*up_bound))
                target_weigh = logo_weigh * target_length / logo_length
                if target_length < bg_length and target_weigh < bg_weigh:
                    break;

            #resize logo img
            #mylogo = imglogo.resize((target_length, target_weigh), Image.ANTIALIAS)
            mylogo = cv2.resize(imglogo,(target_length,target_weigh),interpolation=cv2.INTER_CUBIC)
            #which bg position target paste to 
            point_position_x = random.randint(0, bg_length - target_length)
            point_position_y = random.randint(0, bg_weigh - target_weigh)
            #paste logo
            if mylogo.shape[2] == 3:
                #box = (point_position_x,point_position_y,point_position_x + target_length,point_position_y + target_weigh)
                #imgbg.paste(mylogo, box)
                for i in range(mylogo.shape[0]):
                    for j in range(mylogo.shape[1]):
                        imgbg[i+point_position_x][j+point_position_y][:3] = mylogo[i][j][:3]
            elif mylogo.shape[2] == 4:
                for i in range(mylogo.shape[0]):
                    for j in range(mylogo.shape[1]):
                        if not mylogo[i][j][3] == 0:
                            imgbg[i+point_position_x][j+point_position_y][:3] = mylogo[i][j][:3]
            #cv2.imwrite("/Users/mac/Pictures/test_ball/3.jpg",imglogo)
            cv2.imwrite(img_savepath + '/' + logo_dir_path.split('/')[-1] + '_' + str(count) + '.jpg',imgbg)
            #imgbg.save(img_savepath + '/' + logo_dir_path.split('/')[-1] + '_' + str(count) + '.jpg')
            count += 1

            positioninfo = [logo_dir_path.split('/')[-1],'_',str(count),' ',logo_dir_path.split('/')[-1],' ',
                str(point_position_y),' ',str(point_position_x),' ',str(point_position_y + target_length),' ',str(point_position_x + target_weigh)]
            position_info.append(''.join(positioninfo))
                
            #every type of logo make 500 pages
            if count > picture_count_per_logo:
                print 'logo  ' + logo_dir_path.split('/')[-1] + '  finish!'
                break
        except Exception,e:
            #print e
            continue

#save out position_info
writepathtotxt(position_info)

print 'Done!'
