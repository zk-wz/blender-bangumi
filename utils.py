import bpy

def add_property():
    BangumiSelect = [("bilibili","BiliBili","bilibili"),
                     ("bangumi","Bangumi","bangumi")]
    bpy.types.Scene.source_flag = bpy.props.EnumProperty(items=BangumiSelect, name="选择番剧源", default="bilibili")