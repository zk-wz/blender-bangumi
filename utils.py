
import bpy
from datetime import datetime
from .operators import get_yiyan
from .operators import get_yiyan_saying
from .operators import get_yiyan_source

weekday=datetime.today().isoweekday()

class bangumi_props(bpy.types.PropertyGroup):
    BangumiSelect = [("bilibili","BiliBili","bilibili"),
                     ("bangumi","Bangumi","bangumi")]
    source_flag:bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")
    week_day_flag:bpy.props.BoolProperty(name="显示周历或日历", default=False)
    week_day:bpy.props.IntProperty(name="日期", default=weekday)
    week_pic_scale:bpy.props.FloatProperty(name="周历图片缩放", default=3.5)
    day_pic_scale:bpy.props.FloatProperty(name="日历图片缩放", default=5.0)

    ImgApi_Styles=[
        ("mobile","竖图","竖图"),
        ("pc","横图","横图"),
        ("zsy","自适应","自适应")
    ]
    imgapi_style:bpy.props.EnumProperty(items=ImgApi_Styles, name="图片样式", default="zsy")
    ImgApi_Categories=[
        ("cosplay","Cosplay","cosplay"),
        ("dongman","二次元","二次元"),
        ("fengjing","风景","风景"),
        ("suiji","随机","随机")
    ]
    imgapi_category:bpy.props.EnumProperty(items=ImgApi_Categories, name="图片类型", default="dongman")
    imgapi_scale:bpy.props.FloatProperty(name="图片缩放", default=12.0)

    yiyan=get_yiyan()
    yiyan:bpy.props.StringProperty(name="一言", default=get_yiyan_saying(yiyan))
    yiyan_source:bpy.props.StringProperty(name="一言来源", default=get_yiyan_source(yiyan))

# def add_property():
#     BangumiSelect = [("bilibili","BiliBili","bilibili"),
#                      ("bangumi","Bangumi","bangumi")]
#     bpy.types.Scene.source_flag = bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")