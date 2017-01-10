# coding: utf-8
# this file to make 'voc-like' test.txt,train.txt,trainval.txt,val.txt
# author hanzy 2016_11_10

import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("where_xml",
    help = "in which file u saving your xmls,example:/Users/mac/logo_detection/paste_img/Annotations")
parser.add_argument("where_save_txt",
    help = "in which file u want to save your txts,example:/Users/mac/logo_detection/paste_img/ImageSets/Main")
parser.add_argument("trainval_rate",
    help = "the trainval_rate is,example:0.5")
parser.add_argument("train_rate",
    help = "the train_rate is,example:0.5")
args = parser.parse_args()

# where_xml = '/Users/mac/logo_detection/paste_img/Annotations'
where_xml = args.where_xml

# where_save_txt = '/Users/mac/logo_detection/paste_img/ImageSets/Main'
where_save_txt = args.where_save_txt

# trainval_rate = 0.5
trainval_rate = float(args.trainval_rate)

# train_rate = 0.5
train_rate = float(args.train_rate)

xml_paths = []
train = []
val = []
trainval = []
test = []


def get_xml_path (args, dirname, filenames):
    """
    Callback Function

    @params:
    args : the parameter of os.path.walk(where_xml, get_xml_path, None )
    dirname : folder locations
    filename : filename in folder locations
    """

    # get .xml files
    for filename in filenames:
        if filename[-3:] == 'xml':
            xml_paths.append(filename[:-4])


def writepathtotxt(data_sets, path):
    """

    @params:
    data_sets : the information lists
    path : path to save data_sets
    """

    # use to save data_set infos
    txt_path = path
    with open(txt_path, "w") as f:
        for data_set in data_sets:
            f.write(data_set)
            f.write('\n')

# get xml paths
os.path.walk(where_xml, get_xml_path, None)

for xml_path in xml_paths:
    
    # xml use for test
    if random.randint(0, 100) > trainval_rate * 100:
        test.append(xml_path)
        
    # xml use for trainval
    else:
        trainval.append(xml_path)
        
        # xml use for val
        if random.randint(0, 100) > train_rate * 100:
            val.append(xml_path)
        
        # xml use for train
        else:
            train.append(xml_path)

# save txt
writepathtotxt(test, where_save_txt + '/test.txt')
writepathtotxt(trainval, where_save_txt + '/trainval.txt')
writepathtotxt(val, where_save_txt + '/val.txt')
writepathtotxt(train, where_save_txt + '/train.txt')
