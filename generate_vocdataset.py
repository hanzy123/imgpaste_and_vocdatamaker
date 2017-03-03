from xml.dom.minidom import Document
import os
import random
import argparse
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("dataset_root_dir",
        help = "where u want to save your dataset: example:/Users/mac/logo_detection/mydataset")
parser.add_argument("where_img",
        help = "where your images are: example:/Users/mac/logo_detection/paste_img/new_img")
parser.add_argument("where_positioninfo",
        help = "where your position_info_txt is: example:/Users/mac/logo_detection/paste_img/position_info.txt")
parser.add_argument("trainval_rate",
    help = "the trainval_rate is,example:0.5")
parser.add_argument("train_rate",
    help = "the train_rate is,example:0.5")
args = parser.parse_args()

dataset_root_dir = args.dataset_root_dir

where_img = args.where_img

where_positioninfo = args.where_positioninfo

trainval_rate = float(args.trainval_rate)

train_rate = float(args.train_rate)

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

def generatexml(my_width, my_height, my_depth):
    """

    @params:
    my_width : img_width
    my_height : img_height
    my_depth : img_channel
    """
    # make xml
    doc = Document()

    root = doc.createElement('annotation') 
    doc.appendChild(root)
  
    folder = doc.createElement('folder')
    folder_text = doc.createTextNode('VOC2007')
    folder.appendChild(folder_text)
    root.appendChild(folder)

    filename = doc.createElement('filename')
    filename_text = doc.createTextNode(my_filename)
    filename.appendChild(filename_text)
    root.appendChild(filename)

    # node source
    source = doc.createElement('source')

    database = doc.createElement('database')
    database_text = doc.createTextNode('My Database')
    database.appendChild(database_text)
    source.appendChild(database)

    annotation = doc.createElement('annotation')
    annotation_text = doc.createTextNode('VOC2007')
    annotation.appendChild(annotation_text)
    source.appendChild(annotation)

    image = doc.createElement('image')
    image_text = doc.createTextNode('flickr')
    image.appendChild(image_text)
    source.appendChild(image)

    flickrid = doc.createElement('flickrid')
    flickrid_text = doc.createTextNode('NULL')
    flickrid.appendChild(flickrid_text)
    source.appendChild(flickrid)

    root.appendChild(source)

    # node owner
    owner = doc.createElement('owner')

    flickrid1 = doc.createElement('flickrid')
    flickrid_text1 = doc.createTextNode('NULL')
    flickrid1.appendChild(flickrid_text1)
    owner.appendChild(flickrid1)

    name = doc.createElement('name')
    name_text = doc.createTextNode('sxwl')
    name.appendChild(name_text)
    owner.appendChild(name)

    root.appendChild(owner)

    # node size
    size = doc.createElement('size')

    width = doc.createElement('width')
    width_text = doc.createTextNode(my_width)
    width.appendChild(width_text)
    size.appendChild(width)

    height = doc.createElement('height')
    height_text = doc.createTextNode(my_height)
    height.appendChild(height_text)
    size.appendChild(height)

    depth = doc.createElement('depth')
    depth_text = doc.createTextNode(my_depth)
    depth.appendChild(depth_text)
    size.appendChild(depth)

    root.appendChild(size)

    # node segmented
    segmented = doc.createElement('segmented')
    segmented_text = doc.createTextNode('0')
    segmented.appendChild(segmented_text)
    root.appendChild(segmented)

    # node object
    object1 = doc.createElement('object')

    name1 = doc.createElement('name')
    name_text1 = doc.createTextNode(my_logotype)
    name1.appendChild(name_text1)
    object1.appendChild(name1)

    pose = doc.createElement('pose')
    pose_text = doc.createTextNode('Unspecified')
    pose.appendChild(pose_text)
    object1.appendChild(pose)

    truncated = doc.createElement('truncated')
    truncated_text = doc.createTextNode('0')
    truncated.appendChild(truncated_text)
    object1.appendChild(truncated)

    difficult = doc.createElement('difficult')
    difficult_text = doc.createTextNode('0')
    difficult.appendChild(difficult_text)
    object1.appendChild(difficult)

    bndbox = doc.createElement('bndbox')

    xmin = doc.createElement('xmin')
    xmin_text = doc.createTextNode(my_xmin)
    xmin.appendChild(xmin_text)
    bndbox.appendChild(xmin)

    ymin = doc.createElement('ymin')
    ymin_text = doc.createTextNode(my_ymin)
    ymin.appendChild(ymin_text)
    bndbox.appendChild(ymin)

    xmax = doc.createElement('xmax')
    xmax_text = doc.createTextNode(my_xmax)
    xmax.appendChild(xmax_text)
    bndbox.appendChild(xmax)

    ymax = doc.createElement('ymax')
    ymax_text = doc.createTextNode(my_ymax)
    ymax.appendChild(ymax_text)
    bndbox.appendChild(ymax)

    object1.appendChild(bndbox)

    root.appendChild(object1)

    # output
    f = open(where_save_xml + '/' + my_filename + '.xml','w')
    f.write(doc.toprettyxml())
    f.close()

if __name__ == '__main__':

    xml_paths = []
    train = []
    val = []
    trainval = []
    test = []
    
    # build voc dir structure
    if not os.path.exists(dataset_root_dir + '/VOC2007'):
        os.makedirs(dataset_root_dir + '/VOC2007/Annotations')
        os.makedirs(dataset_root_dir + '/VOC2007/ImageSets/Layout')
        os.makedirs(dataset_root_dir + '/VOC2007/ImageSets/Main')
        os.makedirs(dataset_root_dir + '/VOC2007/ImageSets/Segmentation')
        os.makedirs(dataset_root_dir + '/VOC2007/JPEGImages')
        os.makedirs(dataset_root_dir + '/VOC2007/SegmentationClass')
        os.makedirs(dataset_root_dir + '/VOC2007/SegmentationObject')

    where_save_xml = dataset_root_dir + '/VOC2007/Annotations'
    where_xml = dataset_root_dir + '/VOC2007/Annotations'
    where_save_txt = dataset_root_dir + '/VOC2007/ImageSets/Main'
    JPEGImages_path = dataset_root_dir + '/VOC2007/JPEGImages'
    position_info = open(where_positioninfo, "r")

    while True:   
        # get position info

        positioninfo = position_info.readline()
        positioninfo = positioninfo[:-1]
        if positioninfo:
            my_filename = positioninfo.split(' ')[0]
            #my_filename = my_filename.split('_')[0] + '_' + str(int(my_filename.split('_')[1])-1)
            my_logotype = positioninfo.split(' ')[1]
            my_xmin = positioninfo.split(' ')[2]
            my_ymin = positioninfo.split(' ')[3]
            my_xmax = positioninfo.split(' ')[4]
            my_ymax = positioninfo.split(' ')[5]
        else:
            break

        # get image infomation
        # img = Image.open(where_img + '/' + my_filename + '.jpg')
        img = cv2.imread(where_img + '/' + my_filename + '.jpg')
        my_width = img.shape[1]
        my_height = img.shape[0]
        my_depth = img.shape[2]
        my_width = str(my_width)
        my_height = str(my_height)
        my_depth = str(my_depth)

        # move pictures to dir JPEGImages

        os.system('mv ' + where_img + '/' + my_filename + '.jpg ' + JPEGImages_path)

        # generatexml_path

        generatexml(my_width, my_height, my_depth)

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


