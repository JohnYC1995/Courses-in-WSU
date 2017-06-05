import xml.dom.minidom
from xml.etree import ElementTree as ET
import skimage.io as io
from skimage import data_dir
import random
import os
import math
import skimage as skimage
from skimage import transform, color, exposure
from skimage.transform import rotate
###========annotations==========###
def Get_file_inference(location):
    path = location
    filelist = os.listdir(path)
    filelist.sort()
    return filelist

def Get_Annotation(location):
    per=ET.parse(location)
    p=per.findall('./object')
    Annotations_name = []
    for oneper in p:
        sublistAnnotation = []
        for child in oneper.getchildren():
            if child.tag == 'name':
                sublistAnnotation.append(child.text)
        Annotations_name.append(sublistAnnotation)
    p=per.findall('./object/bndbox')
    Annotations = []
    for oneper in p:
        sublistAnnotation = []
        for child in oneper.getchildren():
            child.text = int(child.text)
            sublistAnnotation.append(child.text)
        Annotations.append(sublistAnnotation)
    label = []
    label_resize = []
    for l in range(len(Annotations)):
        label_resize.append([(int(math.floor(Annotations[l][0]*0.5)),int(math.floor(Annotations[l][1]*0.5))),(int(math.floor(Annotations[l][2]*0.5)),int(math.floor(Annotations[l][3]*0.5)))])
    return label_resize
###=====Image======###
def Get_Image(location):
    coll = io.ImageCollection(location)
    return coll

def get_dataset_size(Annotations_loc,Image_loc):
    labellist = Get_file_inference(Annotations_loc)
    imagelist = Get_file_inference(Image_loc)
    labellist.sort()
    imagelist.sort()
#    print("labellist",labellist)
#    print("imagelist",imagelist)
    if len(labellist) == len(imagelist):
        return len(labellist)
    else:
        return 'Image size does not match with the Annotations '

def get_data():
    Annotations_loc = 'Annotations/'
    Image_loc = 'JPEGImages/'
    max_num = 20
    labellist = []
    imagelist = []
    for index in range(max_num):
        labelfilelist = Get_file_inference(Annotations_loc)
        Anno_Loc = Annotations_loc + labelfilelist[index]
        label_resize = Get_Annotation(Anno_Loc)
        #print("labelresize",label_resize)
        labellist.append(label_resize)
        print("load data:",index,"%",max_num)
        imagefilelist = Get_file_inference(Image_loc)
        image_loc = Image_loc + imagefilelist[index]
        x_shape = Get_Image(image_loc)[0].shape[0]
        y_shape = Get_Image(image_loc)[0].shape[1]
        channel = Get_Image(image_loc)[0].shape[2]
        #print("get_data_image_shape",x_shape,y_shape)

        image =skimage.transform.resize(Get_Image(image_loc)[0],(int(x_shape*0.5),int(y_shape*0.5),channel))
        #print("resize",image.shape)
        imagelist.append(image)
    return labellist,imagelist


if __name__ == "__main__":
    Annotations,image=get_data()

    #Annotations,Annotations_name,image= Data_Generate()
    #print(Annotations[0])
    #print(len(Annotations))
    #print(image[0].shape)
    #print(len(image))



