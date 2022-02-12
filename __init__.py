
bl_info = {
    "name" : "blender-bangumi",
    "author" : "掌控-物质",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from .ui import *
from .operators import *
from .utils import *
import os
from .bangumi_spider import *
from .bilibili_spider import *

classes = [Bilibili_Spider,
           Bangumi_Spider,
           bangumi_n_panel_ui]


def register():
    # print(os.path.dirname(os.path.abspath(__file__)))
    add_property()
    for class_ in classes:
        bpy.utils.register_class(class_)

def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
