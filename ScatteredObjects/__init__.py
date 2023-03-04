bl_info = {
    "name": "Scatter Objects",
    "author": "paula",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Tools",
    "description": "Adds a scatter on a chosen  object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

from . scatter_objects_operator import OT_ScatterObjects
from . apply_scatter_operator import OT_ApplyScatter
from . object_properties import Object_Properties
from . scene_properties import Scene_Properties
from . panel import PT_ScatterObjects
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty
from bpy.types import Scene, Object

# TODO: take a look at https://docs.blender.org/api/current/info_best_practice.html

def register():
    # TODO: group all these classes in a list so register/unregister is way simpler
    register_class(OT_ScatterObjects)
    register_class(OT_ApplyScatter)
    register_class(PT_ScatterObjects)
    register_class(Scene_Properties)
    register_class(Object_Properties)
        
    Scene.properties = PointerProperty(type=Scene_Properties)
    Object.properties = PointerProperty(type=Object_Properties)

def unregister():
    unregister_class(OT_ScatterObjects)
    unregister_class(OT_ApplyScatter)
    unregister_class(PT_ScatterObjects)
    unregister_class(Scene_Properties)
    unregister_class(Object_Properties)
    # TODO: save object props?
    del Scene.properties
    del Object.properties
    
# TODO: necessary?
if __name__ == "__main__":
    register()
