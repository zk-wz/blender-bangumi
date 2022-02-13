import bpy

class bangumi_props(bpy.types.PropertyGroup):
    BangumiSelect = [("bilibili","BiliBili","bilibili"),
                     ("bangumi","Bangumi","bangumi")]
    source_flag:bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")
    week_day_flag:bpy.props.BoolProperty(name="显示周历或日历", default=False)

# def add_property():
#     BangumiSelect = [("bilibili","BiliBili","bilibili"),
#                      ("bangumi","Bangumi","bangumi")]
#     bpy.types.Scene.source_flag = bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")