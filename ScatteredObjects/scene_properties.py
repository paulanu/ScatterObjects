from bpy.props import PointerProperty
from bpy.types import PropertyGroup
import bpy # TODO: maybe import specific thing you need

def filter_callback(self, object):
    return object.name in self.my_collection.objects.keys() and object.type == 'MESH'
    
def clear_my_collection_objects(self, context):
    context.scene.properties.my_collection_objects = None
    
def generate_new_collection(self, context):
    context.scene.properties.current_collection = None
    
class Scene_Properties(PropertyGroup):
    
    #TODO: rename this?
    my_collection: PointerProperty(
        name = "Collection",
        type = bpy.types.Collection,
        update = clear_my_collection_objects
    )
    
    #TODO: rename this to base_obj or something more obvious
    my_collection_objects: PointerProperty(
        name = "Base Object",
        type = bpy.types.Object,
        poll = filter_callback,
        update = generate_new_collection
    )
