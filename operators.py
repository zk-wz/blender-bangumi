import bpy
from .bilibili_spider import *
from .bangumi_spider import *

class Bilibili_Spider(bpy.types.Operator):
    bl_idname = "bangumi_spider.bilibili"
    bl_label = "bilibili_bangumi_spider"
    bl_description = "bilibili番剧爬取"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bilibili_main()
        return {"FINISHED"}

class Bangumi_Spider(bpy.types.Operator):
    bl_idname = "bangumi_spider.bangumi"
    bl_label = "bangumi_bangumi_spider"
    bl_description = "bangumi番剧爬取"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bangumi_main()
        return {"FINISHED"}