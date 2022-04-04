
import bpy
import pickle
import os
import imbuf
from threading import Thread

class Bangumi_Panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Bangumi"

#番剧设置面板        
class Bangumi_Settings(bpy.types.Panel,Bangumi_Panel):
    bl_label = "设定"
    bl_idname = "N_PT_Bangumi_Settings"
    bl_parent_id = "N_PT_Bangumi_Father"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # source_flag=bpy.types.Scene.source_flag
        source_choice = layout.row()
        source_choice.prop(scene.bangumi_property, 'source_flag')

        if scene.bangumi_property.source_flag == 'bilibili':
            source_choice.operator("bangumi.bilibili", text="",icon="FILE_REFRESH")
        elif scene.bangumi_property.source_flag == 'bangumi':
            source_choice.operator("bangumi.bangumi", text="",icon="FILE_REFRESH")
        day_week=source_choice.column()
        day_week.scale_x=0.5

        s=layout.row()
        if scene.bangumi_property.week_day_flag:
            day_week.operator("bangumi.change_calender", text="周历")
            s.prop(scene.bangumi_property,"week_pic_scale")
        else:
            day_week.operator("bangumi.change_calender", text="日历")
            s.prop(scene.bangumi_property,"day_pic_scale")


# 番剧日历面板
class Bangumi_Calendar(bpy.types.Panel,Bangumi_Panel):
    bl_label = "番剧日历"
    bl_idname = "N_PT_Bangumi_Calendar"
    bl_parent_id = "N_PT_Bangumi_Father"

    def draw(self, context):
        layout = self.layout
        scene = context.scene


        #番剧列表
        datelist =["周日","周一","周二","周三","周四","周五","周六"]
        from datetime import datetime
        day=datetime.today().isoweekday()

        bangumi_part = layout.box()
        row=bangumi_part.row()


        if scene.bangumi_property.week_day_flag:

            #把panel拆成七列
            c1=row.column(align=True)
            c2=row.column(align=True)
            c3=row.column(align=True)
            c4=row.column(align=True)
            c5=row.column(align=True)
            c6=row.column(align=True)
            c7=row.column(align=True)
            

            #把七列写进列表
            all_columns = [c1,c2,c3,c4,c5,c6,c7]
            for i in range(7):
                if i==day or (i==0 and day==7):
                    all_columns[i].operator("bangumi.nothing",text="今日",emboss=False)
                else:
                    all_columns[i].operator("bangumi.nothing",text='  ',emboss=False)
            for i in range(7):
                all_columns[i].operator("bangumi.nothing",text=week[i],emboss=False)
            
            pic_scale = scene.bangumi_property.week_pic_scale

            if scene.bangumi_property.source_flag == 'bilibili':
                # info_path=os.path.dirname(os.path.abspath(__file__))+'\\'+'src'+'\\'+'bilibili_info'
                # with open(info_path,"rb") as f:
                #     total_list=pickle.load(f)
                multi_process_loader(all_columns,7,create_bilibili_calendar,pic_scale)
                # for i in range(7):
                #     for j in range(len(bangumi_name["bilibili"][i])):
                #         pic=bangumi_cover["bilibili"]["bilibili_"+week[i]+"_"+str(j)]
                #         all_columns[i].template_icon(pic.icon_id,scale=3.5)
                #         all_columns[i].operator("bangumi.open_bilibili_url",text=bangumi_name["bilibili"][i][j]).flag="+"+str(i)+"_"+str(j)+"-"
            
            else:

                multi_process_loader(all_columns,7,create_bangumi_calendar,pic_scale)
                # for i in range(7):
                #     for j in range(len(bangumi_name["bangumi"][i])):
                #         pic=bangumi_cover["bangumi"]["bangumi_"+week[i]+"_"+str(j)]
                #         all_columns[i].template_icon(pic.icon_id,scale=3.5)
                #         # all_columns[i].label(text=bangumi_name["bangumi"][i][j])
                #         all_columns[i].operator("bangumi.open_bangumi_url",text=bangumi_name["bangumi"][i][j]).bangumi_flag="+"+str(i)+"_"+str(j)+"-"



        else:
            cl=row.column()
            cc=row.column()
            cr=row.column()

            if scene.bangumi_property.week_day==7:
                i=0
            else:
                i=scene.bangumi_property.week_day
            cl.operator("bangumi.previous_day",text='',icon="TRIA_LEFT")
            cc.operator("bangumi.nothing",text=datelist[i],emboss=False)
            cr.operator("bangumi.next_day",text='',icon="TRIA_RIGHT")

            pic_scale = scene.bangumi_property.day_pic_scale

            if scene.bangumi_property.source_flag == 'bilibili':
                for j in range(len(bangumi_name["bilibili"][i])):
                    pic=bangumi_cover["bilibili"]["bilibili_"+week[i]+"_"+str(j)]
                    cc.template_icon(pic.icon_id,scale=pic_scale)
                    cc.operator("bangumi.open_bilibili_url",text=bangumi_name["bilibili"][i][j]).flag="+"+str(i)+"_"+str(j)+"-"

            else:
                for j in range(len(bangumi_name["bangumi"][i])):
                    pic=bangumi_cover["bangumi"]["bangumi_"+week[i]+"_"+str(j)]
                    cc.template_icon(pic.icon_id,scale=pic_scale)
                    cc.operator("bangumi.open_bangumi_url",text=bangumi_name["bangumi"][i][j]).bangumi_flag="+"+str(i)+"_"+str(j)+"-"   

        

#番剧总面板
class bangumi_n_father_panel(bpy.types.Panel,Bangumi_Panel):
    bl_label = "每周番剧表"
    bl_idname = "N_PT_Bangumi_Father"


    def draw_header(self,context):
        layout = self.layout
        layout.label(text="",icon='KEYTYPE_KEYFRAME_VEC')
        # return super().draw_header(context)

    def draw(self, context):
        layout = self.layout.box().column(align=True)
        layout.operator("bangumi.copy_text",text=context.scene.bangumi_property.yiyan,emboss=False)
        layout.operator("bangumi.nothing",text=context.scene.bangumi_property.yiyan_source,emboss=False)


#随机涩图总面板
class rand_img_father_panel(bpy.types.Panel,Bangumi_Panel):
    bl_idname = "N_PT_Rand_Img_Father"
    bl_label = "随机涩图"

    def draw_header(self,context):
        self.layout.label(text="",icon='FUND')

    def draw(self, context):
        pass
        
#随机涩图设置面板
class Rand_Img_Settings(bpy.types.Panel,Bangumi_Panel):
    bl_idname = "N_PT_Rand_Img_Settings"
    bl_label = "设定"
    bl_parent_id = "N_PT_Rand_Img_Father"

    def draw(self, context):
        layout = self.layout
        bangumi_property = context.scene.bangumi_property

        row1=layout.row()
        if bangumi_property.imgapi_category != "cosplay":
            style = row1.column()
            style.prop(bangumi_property,"imgapi_style")

        category=row1.column()
        category.prop(bangumi_property,"imgapi_category")

        row2=layout.row()
        scale=row2.column()
        scale.prop(bangumi_property,"imgapi_scale")

        refresh=row2.column()
        refresh.operator("bangumi.imgapi_refresh",text="",icon='FILE_REFRESH')

        row3=layout.row()
        row3.operator("bangumi.switch_to_img_editor",icon="OUTLINER_OB_IMAGE")

        
#随机涩图图片显示面板
class Rand_Img_Pic(bpy.types.Panel,Bangumi_Panel):
    bl_idname = "N_PT_Rand_Img_Pic"
    bl_label = "图片"
    bl_parent_id = "N_PT_Rand_Img_Father"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.box()
        pic = other_pic["imgapi"]["rand_img"]
        pic_scale = context.scene.bangumi_property.imgapi_scale
        layout.template_icon(pic.icon_id,scale=pic_scale)

#随机涩图图像编辑器总面板
class imgeditor_randimg_father(bpy.types.Panel):
    bl_idname = "N_PT_ImgEditor_RandImg_Father"
    bl_label = "随机涩图"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "涩涩"

    def draw_header(self,context):
        self.layout.label(text="",icon='FUND')

    def draw(self, context):
        layout = self.layout
        bangumi_property = context.scene.bangumi_property

        style=layout.row()
        if bangumi_property.imgapi_category != "cosplay":
            style.prop(bangumi_property,"imgapi_style")

        category=layout.row()
        category.prop(bangumi_property,"imgapi_category")

        refresh=layout.row()
        refresh.operator("bangumi.img_editor_rand_img_refresh",icon='FILE_REFRESH')

        row3=layout.row()
        row3.operator("bangumi.quick_switch",icon='ERROR')





class yiyan_father_panel(bpy.types.Panel,Bangumi_Panel):
    bl_idname = "N_PT_Yiyan_Father"
    bl_label = "一言"

    def draw_header(self,context):
        self.layout.label(text="",icon='INFO')

    def draw(self, context):
        pass

class Yiyan_Settings(bpy.types.Panel,Bangumi_Panel):
    bl_idname = "N_PT_Yiyan_Settings"
    bl_label = "设定"
    bl_parent_id = "N_PT_Yiyan_Father"

    def draw(self, context):
        layout = self.layout
        row=layout.row()
        row.operator("bangumi.refresh_yiyan",icon='FILE_REFRESH')
                

class Yiyan(bpy.types.Panel,Bangumi_Panel):
    bl_idname = "N_PT_Yiyan"
    bl_label = "一言"
    bl_parent_id = "N_PT_Yiyan_Father"


    def draw(self, context):
        layout = self.layout.box().column(align=True)
        layout.operator("bangumi.copy_text",text=context.scene.bangumi_property.yiyan,emboss=False)
        layout.operator("bangumi.nothing",text=context.scene.bangumi_property.yiyan_source,emboss=False)
        


def create_bilibili_calendar(all_columns,i,pic_scale):

    for j in range(len(bangumi_name["bilibili"][i])):
        pic=bangumi_cover["bilibili"]["bilibili_"+week[i]+"_"+str(j)]
        all_columns[i].template_icon(pic.icon_id,scale=pic_scale)
        all_columns[i].operator("bangumi.open_bilibili_url",text=bangumi_name["bilibili"][i][j]).flag="+"+str(i)+"_"+str(j)+"-"


def create_bangumi_calendar(all_columns,i,pic_scale):

    for j in range(len(bangumi_name["bangumi"][i])):
        pic=bangumi_cover["bangumi"]["bangumi_"+week[i]+"_"+str(j)]
        all_columns[i].template_icon(pic.icon_id,scale=pic_scale)
        all_columns[i].operator("bangumi.open_bangumi_url",text=bangumi_name["bangumi"][i][j]).bangumi_flag="+"+str(i)+"_"+str(j)+"-"


def multi_process_loader(all_columns,tread_num,target,pic_scale):

    treads = []
    for i in range(tread_num):
        treads.append(Thread(target=target, args=(all_columns,i,pic_scale)))
    for i in treads:
        i.start()
    for i in treads:
        i.join()



bangumi_name = {}
bangumi_cover = {}
other_pic = {}
week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def refresh_name(platform):
    if platform == 'bilibili':
        info_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),'bilibili_info')
        with open(info_path,"rb") as f:
            total_list=pickle.load(f)
        bangumi_name["bilibili"]=total_list[0]
    elif platform == 'bangumi':
        info_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),'bangumi_info')
        with open(info_path,"rb") as f:
            total_list=pickle.load(f)
        bangumi_name["bangumi"]=total_list[0]

def ui_register():
    refresh_name("bilibili")
    refresh_name("bangumi")

    #将bilibili番剧封面导入为blender icon
    bilibili_info_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),'bilibili_info')
    with open(bilibili_info_path,"rb") as f:
        bilibili_total_list=pickle.load(f)
    pcoll = bpy.utils.previews.new()
    for i in range(7):
        for j in range(len(bilibili_total_list[0][i])):
            bilibili_pic_path=os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "bilibili"), week[i]), str(j)+'.jpg')
            error_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "error.png")
            try:
                if not os.path.exists(bilibili_pic_path):
                    img=imbuf.load(error_path)
                    imbuf.write(image=img,filepath=bilibili_pic_path)
            except:
                print('error')

            pcoll.load("bilibili_"+week[i]+"_"+str(j), bilibili_pic_path, 'IMAGE')

    bangumi_cover["bilibili"]=pcoll


    #将bangumi番剧封面导入为blender icon
    bangumi_info_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'),'bangumi_info')
    with open(bangumi_info_path,"rb") as f:
        bangumi_total_list=pickle.load(f)
    bgm = bpy.utils.previews.new()
    for i in range(7):
        for j in range(len(bangumi_total_list[0][i])):
            bangumi_pic_path=os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "bangumi"), week[i]), str(j)+'.jpg')
            error_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "error.png")
            try:
                if not os.path.exists(bangumi_pic_path):
                    img=imbuf.load(error_path)
                    imbuf.write(image=img,filepath=bangumi_pic_path)

                img=imbuf.load(bangumi_pic_path)
                width=img.size[0]
                height=img.size[1]
                if width != height:
                    img_size=min(width,height)-1
                    x_min=int(width/2-img_size/2)
                    y_min=int(height/2-img_size/2)
                    x_max=int(width/2+img_size/2)
                    y_max=int(height/2+img_size/2)
                    img.crop((x_min,y_min),(x_max,y_max))
                    imbuf.write(image=img,filepath=bangumi_pic_path)
            except:
                print('error')

            bgm.load("bangumi_"+week[i]+"_"+str(j), bangumi_pic_path, 'IMAGE')

    bangumi_cover["bangumi"]=bgm


def ui_unregister():
    for pcoll in bangumi_cover.values():
        bpy.utils.previews.remove(pcoll)
    bangumi_cover.clear()


# 将imgapi封面导入为blender icon
def imgapi_register():
    imgapi_pic2icon = bpy.utils.previews.new()
    imgapi_pic_path=os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "rand_img"), 'rand_img.jpg')
    error_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "error.png")
    try:
        if not os.path.exists(imgapi_pic_path):
            img=imbuf.load(error_path)
            imbuf.write(image=img,filepath=imgapi_pic_path)
    except:
        print('error')

    imgapi_pic2icon.load("rand_img", imgapi_pic_path, 'IMAGE')
    other_pic["imgapi"]=imgapi_pic2icon


def imgapi_unregister():
    for pcoll in other_pic.values():
        bpy.utils.previews.remove(pcoll)
    other_pic.clear()