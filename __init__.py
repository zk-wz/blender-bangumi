
bl_info = {
    "name" : "blender-bangumi",
    "author" : "掌控-物质",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Bangumi"
}

# import bpy
from .ui import *
from .operators import *
from .utils import *
import os
from .bangumi_spider import *
from .bilibili_spider import *
import pickle
import bpy.utils.previews

classes = [Bilibili_Spider,
           Bangumi_Spider,
           bangumi_n_panel_ui]
week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

bangumi_cover = {}

def register():
    # print(os.path.dirname(os.path.abspath(__file__)))
    add_property()


    bilibili_info_path=os.path.dirname(os.path.abspath(__file__))+'\\'+'src'+'\\'+'bilibili_info'
    bilibili_total_list=pickle.load(open(bilibili_info_path,"rb"))
    pcoll = bpy.utils.previews.new()
    for i in range(7):
        for j in range(len(bilibili_total_list[0][i])):
            bilibili_pic_name=str(j)+'.jpg'
            bilibili_pic_path=os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "bilibili"), week[i]), bilibili_pic_name)
            pcoll.load("bilibili_"+week[i]+"_"+str(j), bilibili_pic_path, 'IMAGE')
            bangumi_cover["bilibili_"+week[i]+"_"+str(j)]=pcoll


    bangumi_info_path=os.path.dirname(os.path.abspath(__file__))+'\\'+'src'+'\\'+'bangumi_info'
    bangumi_total_list=pickle.load(open(bangumi_info_path,"rb"))
    for i in range(7):
        for j in range(len(bangumi_total_list[2][i])):
            bangumi_pic_name=str(j)+'.jpg'
            bangumi_pic_path=os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "bangumi"), week[i]), bangumi_pic_name)
            pcoll.load("bangumi_"+week[i]+"_"+str(j), bangumi_pic_path, 'IMAGE')
            bangumi_cover["bangumi_"+week[i]+"_"+str(j)]=pcoll


    for class_ in classes:
        bpy.utils.register_class(class_)

def unregister():

    # for pcoll in bangumi_cover.values():
    #     bpy.utils.previews.remove(pcoll)
    # bangumi_cover.clear()

    for class_ in classes:
        bpy.utils.unregister_class(class_)
