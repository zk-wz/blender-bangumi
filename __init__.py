# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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

classes = [bangumi_n_panel_ui,
           Bilibili_Spider,
           Bangumi_Spider]


def register():
    # print(os.path.dirname(os.path.abspath(__file__)))
    add_property()
    for class_ in classes:
        bpy.utils.register_class(class_)

def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
