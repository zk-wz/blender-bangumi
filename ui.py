import bpy
import pickle
import os

class bangumi_n_panel_ui(bpy.types.Panel):
    bl_label = "每周番剧表"
    bl_idname = "N_PT_UI"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "bangumi"

    # BangumiSelect = [("bilibili","BiliBili","bilibili"),
    #                  ("bangumi","Bangumi","bangumi")]
    # source_flag:bpy.props.EnumProperty(items=BangumiSelect, name="番剧源", default="bilibili")

    def draw_header(self,context):
        layout = self.layout
        layout.label(text="",icon='FUND')
        # return super().draw_header(context)

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        # source_flag=bpy.types.Scene.source_flag
        source_choice = layout.row()
        source_choice.prop(scene, 'source_flag')

        if scene.source_flag == 'bilibili':
            source_choice.operator("bangumi_spider.bilibili", text="",icon="FILE_REFRESH")
        elif scene.source_flag == 'bangumi':
            source_choice.operator("bangumi_spider.bangumi", text="",icon="FILE_REFRESH")

        #番剧列表
        datelist =["周日","周一","周二","周三","周四","周五","周六"]
        bangumi_part = layout.box()
        #把panel拆成七列
        row=bangumi_part.row()

        c1=row.column(align=True)
        c2=row.column(align=True)
        c3=row.column(align=True)
        c4=row.column(align=True)
        c5=row.column(align=True)
        c6=row.column(align=True)
        c7=row.column(align=True)
        
        from datetime import datetime
        day=datetime.today().isoweekday()


        #把七列写进列表
        all_columns = [c1,c2,c3,c4,c5,c6,c7]
        for i in range(7):
            if i==day or (i==0 and day==7):
                all_columns[i].label(text="今日")
            else:
                all_columns[i].label(text='  ')
        for i in range(7):
            all_columns[i].label(text=datelist[i])
        
        week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        if scene.source_flag == 'bilibili':
            path=os.path.dirname(os.path.abspath(__file__))+'\\'+'src'+'\\'+'bilibili_info'
            total_list=pickle.load(open(path,"rb"))
            for i in range(7):
                for j in range(len(total_list[0][i])):
                    all_columns[i].template_icon(text="",icon_value=bangumi_cover["bilibili_"+week[i]+"_"+str(j)]["bilibili_"+week[i]+"_"+str(j)].icon_id)
        elif scene.source_flag == 'bangumi':
            path=os.path.dirname(os.path.abspath(__file__))+'\\'+'src'+'\\'+'bangumi_info'
            total_list=pickle.load(open(path,"rb"))


