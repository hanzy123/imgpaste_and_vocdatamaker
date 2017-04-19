    # coding: utf-8
# this file to make paste-logo images
# author hanzy 2016_11_10

import cv2
import random
import os
import numpy as np
import argparse
import copy
import random
from skimage import data, exposure, img_as_float

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
# lower_bound = 0.2
lower_bound = args.lower_bound
# up_bound = 0.4
up_bound = args.up_bound
# picture_count_per_logo = 3000
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

def horizontal_flip(imglogo):
    """水平翻转
    Args:
        imglogo (ndarray)
    Return:
        imglogo (ndarray)
    """
    for i in xrange(imglogo.shape[0]):
        for j in xrange(imglogo.shape[1]/2):
            mid = copy.deepcopy(imglogo[i][j])
            imglogo[i][j] = imglogo[i][imglogo.shape[1] - j - 1]
            imglogo[i][imglogo.shape[1] - j - 1] = mid
    return imglogo

def vertical_flip(imglogo):
    """垂直翻转
    Args:
        imglogo (ndarray)
    Return:
        imglogo (ndarray)
    """
    for i in xrange(imglogo.shape[0]/2):
        for j in xrange(imglogo.shape[1]):
            mid = copy.deepcopy(imglogo[i][j])
            imglogo[i][j] = imglogo[imglogo.shape[0]-i-1][j]
            imglogo[imglogo.shape[0]-i-1][j] = mid
    return imglogo

def modify_lightness(imglogo, alpha):
    """修改明暗度
    Args:
        imglogo (ndarray)
        alpha (float) : 0 ~ 10+,0~1,调亮，1～10+调暗
    Return:
        gam (ndarray)
    """
    img = img_as_float(imglogo)
    gam= exposure.adjust_gamma(img, alpha)
    return gam

def image_rotate(imglogo, degree):
    """旋转
    Args:
        imglogo (ndarray)
        degree (float)
    Return:
        dst (ndarray)
    """
    rows,cols,depth = imglogo.shape
    degree = 90
    M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,1)
    dst = cv2.warpAffine(imglogo,M,(cols,rows))
    return dst

def pre_process(imglogo):
    """预处理图片
    Args:
        imglogo (ndarry) 
    """
    #process_list = ['nothing','horizontal_flip', 'vertical_flip', 'modify_lightness', 'image_rotate']
    process_list = ['nothing','horizontal_flip', 'vertical_flip', 'image_rotate']
    process_id = random.randint(0,3)
    if process_list[process_id] == 'nothing':
        print "do nothing"
    elif process_list[process_id] == 'horizontal_flip':
        imglogo = horizontal_flip(imglogo)
    elif process_list[process_id] == 'vertical_flip':
        imglogo = vertical_flip(imglogo)
    elif process_list[process_id] == 'modify_lightness':
        alpha = random.uniform(0.1,2.0)
        imglogo = modify_lightness(imglogo, alpha)
    elif process_list[process_id] == 'image_rotate':
        degree = random.randint(1,359)
        imglogo = image_rotate(imglogo, degree)
    return imglogo



def resize_img(imglogo, imgbg):
    """resize imglogo
    Args:
        imglogo (ndarray) 
        imgbg (ndarray)
    Return:
        mylogo (ndarray)
    """
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
    mylogo = cv2.resize(imglogo,(target_length,target_weigh),interpolation=cv2.INTER_CUBIC)    
    return mylogo,bg_length,bg_weigh,target_length,target_weigh
def paste_img(mylogo):
    """paste the front img to bg img
    Args:
        mylogo (ndarray)
    Return:
        imgbg (ndarray) : has the same shape as bg img
    """
    if mylogo.shape[2] == 3:
        for i in range(mylogo.shape[0]):
            for j in range(mylogo.shape[1]):
                imgbg[i+point_position_x][j+point_position_y][:3] = mylogo[i][j][:3]
    elif mylogo.shape[2] == 4:
        for i in range(mylogo.shape[0]):
            for j in range(mylogo.shape[1]):
                if not mylogo[i][j][3] == 0:
                    imgbg[i+point_position_x][j+point_position_y][:3] = mylogo[i][j][:3]
    return imgbg


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
            
            # resize img
            mylogo,bg_length,bg_weigh,target_length,target_weigh = resize_img(imglogo, imgbg)

            # preprocess img
            mylogo = pre_process(mylogo)
            mylogo = pre_process(mylogo)

	        # which bg position target paste to
            point_position_x = random.randint(0, bg_length - target_length)
            point_position_y = random.randint(0, bg_weigh - target_weigh)
            # paste logo
            imgbg = paste_img(mylogo)
	        # modify picture lightness
            alpha = random.uniform(0.5,1.5)
            imglogo = modify_lightness(imglogo, alpha)            
	        # save out image
            cv2.imwrite(img_savepath + '/' + logo_dir_path.split('/')[-1] + '_' + str(count) + '.jpg',imgbg)
            print "save img id ====== " + str(count)
            count += 1
            # save out positioninfo(list)
            positioninfo = [logo_dir_path.split('/')[-1],'_',str(count),' ',logo_dir_path.split('/')[-1],' ',
                str(point_position_y),' ',str(point_position_x),' ',str(point_position_y + target_length),' ',str(point_position_x + target_weigh)]
            position_info.append(''.join(positioninfo))
                
            #every type of logo make 500 pages
            if count > picture_count_per_logo:
                print 'logo  ' + logo_dir_path.split('/')[-1] + '  finish!'
                break
        except Exception,e:
            print e
            continue

#save out position_info
writepathtotxt(position_info)

print 'Done!'
