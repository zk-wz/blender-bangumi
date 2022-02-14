import bpy
from datetime import datetime

weekday=datetime.today().isoweekday()

class bangumi_props(bpy.types.PropertyGroup):
    BangumiSelect = [("bilibili","BiliBili","bilibili"),
                     ("bangumi","Bangumi","bangumi")]
    source_flag:bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")
    week_day_flag:bpy.props.BoolProperty(name="显示周历或日历", default=False)
    week_day:bpy.props.IntProperty(name="日期", default=weekday)
    week_pic_scale:bpy.props.FloatProperty(name="周历图片缩放", default=3.5)
    day_pic_scale:bpy.props.FloatProperty(name="日历图片缩放", default=5.0)

# def add_property():
#     BangumiSelect = [("bilibili","BiliBili","bilibili"),
#                      ("bangumi","Bangumi","bangumi")]
#     bpy.types.Scene.source_flag = bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")