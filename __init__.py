
bl_info = {
    "name" : "blender-bangumi",
    "author" : "掌控-物质",
    "description" : "能让你在blender更方便的追（mo）番（yu）",
    "blender" : (2, 80, 0),
    "version" : (1, 1, 0),
    "location" : "",
    "warning" : "",
    "category" : "Bangumi"
}

# import bpy
from .ui import *
from .operators import *
from .utils import *
from .bangumi_spider import *
from .bilibili_spider import *
# import bpy.utils.previews


classes = [bangumi_props,
           Bilibili_Spider,
           Open_bilibili_url,
           Open_bangumi_url,
           Bangumi_Spider,
           Change_calender,
           bangumi_n_father_panel,
           Bangumi_Settings,
           Bangumi_Calendar,
           Next_Day,
           Previous_Day,
           Nothing]



def register():

    # add_property()
    ui_register()
    operator_register()
    for class_ in classes:
        bpy.utils.register_class(class_)

    bpy.types.Scene.bangumi_property = bpy.props.PointerProperty(type=bangumi_props)

def unregister():

    for pcoll in bangumi_cover.values():
        bpy.utils.previews.remove(pcoll)
    bangumi_cover.clear()

    for class_ in classes:
        bpy.utils.unregister_class(class_)
