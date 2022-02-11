import bpy


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
        s1=bangumi_part.split(factor=0.134)
        c1=s1.column()
        
        s2=s1.split(factor=0.15)
        c2=s2.column()
        
        s3=s2.split(factor=0.19)
        c3=s3.column()
        
        s4=s3.split(factor=0.24)
        c4=s4.column()
        
        s5=s4.split(factor=0.3)
        c5=s5.column()
        
        s6=s5.split(factor=0.5)
        c6=s6.column()
        
        c7=s6.column()

        #把七列写进列表
        all_columns = [c1,c2,c3,c4,c5,c6,c7]
        for i in range(7):
            all_columns[i].label(text=datelist[i])

        if scene.source_flag == 'bilibili':
            pass
        elif scene.source_flag == 'bangumi':
            pass



