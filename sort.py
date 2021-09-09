import os
import cv2
from xml.dom.minidom import parse
import xml.dom.minidom

type_list = ['continuous tin', 'pseudo soldering', 'missing part']

def get_typeindex(typename):#函数用于获取种类索引号(0-2)
    # type_list = ['continuous tin', 'pseudo soldering', 'missing part']
    return type_list.index(typename)

# class Object:
#     def __init__(self,typename,xmin,ymin,xmax,ymax):
#         self.typename = typename
#         self.xmin = xmin
#         self.ymin = ymin
#         self.xmax = xmax
#         self.ymax = ymax
#     def get_typeindex(self):
#         type_list = ['continuous tin', 'pseudo soldering', 'missing part']
#         return type_list.index(self.typename)

#声明标注文档文件夹地址、代切割图片文件夹地址与目标种类文件夹地址
Annotation_dir = './Annotations/'
img_dir = './images/'
sorted_path = ['./continuous tin/','./pseudo soldering/','./missing part/']
#获取所有文档名称与图片名称
xml_list = os.listdir(Annotation_dir)
img_list = os.listdir(img_dir)
# print(xml_list,img_list)


# print("文件名 标注文档位置 图片位置")
#按文件名迭代切割
for item in xml_list:
    file_name = item.split('.')[0]#文件名
    annotations_path = os.path.join(Annotation_dir,item)#标注文档路径
    img_path = os.path.join(img_dir,file_name + '.jpg')#代切割图片路径
    # print(file_name,annotations_path,img_path)
    img = cv2.imread(img_path)#使用cv2获取带切割图片
    
    '''xml解析获取所有标注目标'''
    # Annotations = xml.dom.minidom.parse('C:/Users/houzs/Desktop/目标检测/已标注/已标注/Annotations/20210810133819515PCB.xml')
    Annotations = xml.dom.minidom.parse(annotations_path)
    annotations = Annotations.documentElement
    objects_list = annotations.getElementsByTagName("object")
    type_count =[0,0,0]#已知种类个数
    for object_item in objects_list:
        type_name = object_item.getElementsByTagName('name')[0].childNodes[0].data
        type_index = get_typeindex(type_name)
        '''获取长方形bndbox左上、左下、右上、右下四点位置'''
        bndbox = object_item.getElementsByTagName('bndbox')[0]
        xmin = int(bndbox.getElementsByTagName('xmin')[0].childNodes[0].data)
        ymin = int(bndbox.getElementsByTagName('ymin')[0].childNodes[0].data)
        xmax = int(bndbox.getElementsByTagName('xmax')[0].childNodes[0].data)
        ymax = int(bndbox.getElementsByTagName('ymax')[0].childNodes[0].data)
        cropped = img[ymin:ymax,xmin:xmax]#切割图片
        #分配文件名
        object_path = sorted_path[type_index] + file_name + '_' + str(type_index).zfill(2) +"_" + str(type_count[type_index]).zfill(2) +".jpg"
        cv2.imwrite(object_path,cropped)#写入
        type_count[type_index] += 1
