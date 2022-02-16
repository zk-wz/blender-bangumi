import bpy
from .bilibili_spider import *
from .bangumi_spider import *
import os
import pickle
import webbrowser
import re
from . import ui
from datetime import datetime
from . import imgapi_spider
import random

class Nothing(bpy.types.Operator):
    bl_idname = "bangumi.nothing"
    bl_label = "Nothing"
    bl_description = "啥都不会发生"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {"FINISHED"}


class Refresh_Yiyan(bpy.types.Operator):
    bl_idname = "bangumi.refresh_yiyan"
    bl_label = "刷新一言"
    bl_description = "刷新一言"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        yiyan=get_yiyan()
        context.scene.bangumi_property.yiyan=get_yiyan_saying(yiyan)
        context.scene.bangumi_property.yiyan_source=get_yiyan_source(yiyan)
        return {"FINISHED"}



class Next_Day(bpy.types.Operator):
    bl_idname = "bangumi.next_day"
    bl_label = "next_day"
    bl_description = "下一天"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if context.scene.bangumi_property.week_day!=7:
            context.scene.bangumi_property.week_day += 1
        else:
            context.scene.bangumi_property.week_day = 1
        return {"FINISHED"}


class Previous_Day(bpy.types.Operator):
    bl_idname = "bangumi.previous_day"
    bl_label = "previous_day"
    bl_description = "上一天"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if context.scene.bangumi_property.week_day!=1:
            context.scene.bangumi_property.week_day -= 1
        else:
            context.scene.bangumi_property.week_day = 7
        return {"FINISHED"}


class Imgapi_Refresh(bpy.types.Operator):
    bl_idname = "bangumi.imgapi_refresh"
    bl_label = "刷新图片"
    bl_description = "刷新图片"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ui.imgapi_unregister()

        bangumi_property=context.scene.bangumi_property
        imgapi_spider.imgapi_dl(bangumi_property.imgapi_style,bangumi_property.imgapi_category)

        ui.imgapi_register()
        return {"FINISHED"}


class ImgEditor_RandImg_Refresh(bpy.types.Operator):
    bl_idname = "bangumi.img_editor_rand_img_refresh"
    bl_label = "刷新图片"
    bl_description = "刷新图片"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ui.imgapi_unregister()

        bangumi_property=context.scene.bangumi_property
        imgapi_spider.imgapi_dl(bangumi_property.imgapi_style,bangumi_property.imgapi_category)

        if not test_img_exist():
            pic_path=os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "rand_img"), "rand_img.jpg")
            bpy.ops.image.open(filepath=pic_path)

        bpy.ops.image.reload()

        try:
            bpy.data.images["rand_img.jpg"].colorspace_settings.name = "Utility - sRGB - Texture"
        except:
            bpy.data.images["rand_img.jpg"].colorspace_settings.name = "sRGB"

        ui.imgapi_register()
        return {"FINISHED"}


class Quick_Switch(bpy.types.Operator):
    bl_idname = "bangumi.quick_switch"
    bl_label = "防社死"
    bl_description = "防社死"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.area.ui_type = "VIEW_3D"
        return {"FINISHED"}


class Switch_to_ImgEditor(bpy.types.Operator):
    bl_idname = "bangumi.switch_to_img_editor"
    bl_label = "在图像编辑器中打开"
    bl_description = "在图像编辑器中打开"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not test_img_exist():
            pic_path=os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "rand_img"), "rand_img.jpg")
            bpy.ops.image.open(filepath=pic_path)

        bpy.ops.image.reload()

        try:
            bpy.data.images["rand_img.jpg"].colorspace_settings.name = "Utility - sRGB - Texture"
        except:
            bpy.data.images["rand_img.jpg"].colorspace_settings.name = "sRGB"
        return {"FINISHED"}




class Change_calender(bpy.types.Operator):
    bl_idname = "bangumi.change_calender"
    bl_label = "change_calender"
    bl_description = "切换日历显示样式"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        if(context.scene.bangumi_property.week_day_flag == True):
            context.scene.bangumi_property.week_day_flag = False
        else:
            context.scene.bangumi_property.week_day_flag = True
            context.scene.bangumi_property.week_day = datetime.today().isoweekday()

        return {"FINISHED"}



class Bilibili_Spider(bpy.types.Operator):
    bl_idname = "bangumi.bilibili"
    bl_label = "bilibili_bangumi_spider"
    bl_description = "bilibili数据更新"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bilibili_main()
        ui.ui_unregister()
        ui.ui_register()
        get_link_bilibili()
        self.report({'INFO'}, "数据更新完成")
        return {"FINISHED"}

class Bangumi_Spider(bpy.types.Operator):
    bl_idname = "bangumi.bangumi"
    bl_label = "bangumi_bangumi_spider"
    bl_description = "bangumi数据更新"
    bl_options = {"REGISTER"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bangumi_main()
        ui.ui_unregister()
        ui.ui_register()
        get_link_bangumi()
        self.report({'INFO'}, "数据更新完成")
        return {"FINISHED"}



class Open_bilibili_url(bpy.types.Operator):
    bl_idname = "bangumi.open_bilibili_url"
    bl_label = "open_bilibili_url"
    bl_description = "在浏览器中打开该番剧页面"
    bl_options = {"REGISTER"}

    flag:bpy.props.StringProperty(name='flag', default='0')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #实在不知道怎么往这里面传参了，不得已用上了这个离大谱的办法，知道咋办的兄弟救一下plz!!!!!!!!!!
        #2022.2.16追加：才想起来可以用全局的RNA属性来着，我怕不是个傻子
        i=int(re.search(r"\+.*?_",self.flag).group()[1:-1])
        j=int(re.search(r"_.*?-",self.flag).group()[1:-1])
        webbrowser.open(url = bilibili_link_list[0][i][j], new = 0)
        return {"FINISHED"}
        


class Open_bangumi_url(bpy.types.Operator):
    bl_idname = "bangumi.open_bangumi_url"
    bl_label = "open_bangumi_url"
    bl_description = "在浏览器中打开该番剧页面"
    bl_options = {"REGISTER"}

    bangumi_flag:bpy.props.StringProperty(name='bangumi_flag', default='0')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        x=int(re.search(r"\+.*?_",self.bangumi_flag).group()[1:-1])
        y=int(re.search(r"_.*?-",self.bangumi_flag).group()[1:-1])
        webbrowser.open(url = bangumi_link_list[0][x][y], new = 0)
        return {"FINISHED"}


def test_img_exist():
    for i in bpy.data.images:
        if i.name == "rand_img.jpg":
            return True
    return False


def get_yiyan():
    yiyan_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"), "yiyan")
    with open(yiyan_path,"rb") as f:
        yiyan_list=pickle.load(f)
    return random.choice(yiyan_list)

def get_yiyan_saying(yiyan):
    flag=yiyan.find("\n")
    return yiyan[:flag]

def get_yiyan_source(yiyan):
    flag=yiyan.find("\n")
    return "    "+yiyan[flag+1:]

bilibili_link_list={}
bangumi_link_list={}

def get_link_bilibili():
    bilibili_info_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),'bilibili_info')
    with open(bilibili_info_path,'rb') as f:
        total_list=pickle.load(f)
        bilibili_link_list[0]=total_list[2]

def get_link_bangumi():
    bangumi_info_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),'bangumi_info')
    with open(bangumi_info_path,'rb') as f:
        total_list=pickle.load(f)
        bangumi_link_list[0]=total_list[2]



def operator_register():
    get_link_bilibili()
    get_link_bangumi()
