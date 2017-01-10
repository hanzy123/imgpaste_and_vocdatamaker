# coding: utf-8
# this file to make 'voc-like' xmlfile 
# author hanzy 2016_11_10

from xml.dom.minidom import Document
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("where_save_xml",
        help = "where do u want to save your xmls: example:/Users/mac/logo_detection/paste_img/Annotations")
parser.add_argument("where_img",
        help = "where your images are: example:/Users/mac/logo_detection/paste_img/new_img")
parser.add_argument("where_positioninfo",
        help = "where your position_info_txt is: example:/Users/mac/logo_detection/paste_img/position_info.txt")
args = parser.parse_args()

# where_save_xml = '/Users/mac/logo_detection/paste_img/Annotations'
where_save_xml = args.where_save_xml

# where_img = '/Users/mac/logo_detection/paste_img/new_img'
where_img = args.where_img

# where_positioninfo = '/Users/mac/logo_detection/paste_img/position_info.txt'
where_positioninfo = args.where_positioninfo

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
    # get image info
    img = Image.open(where_img + '/' + my_filename + '.jpg')
    my_width,my_height = img.size
    my_depth = img.layers
    my_width = str(my_width)
    my_height = str(my_height)
    my_depth = str(my_depth)

    
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

