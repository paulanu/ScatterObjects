import bpy # TODO: maybe import specific thing you need
from bpy.props import (
    FloatProperty,
    PointerProperty,
    StringProperty,
    IntProperty
)
from bpy.types import PropertyGroup

def get_object_properties_and_node_tree(context):
    props = context.scene.properties.my_collection_objects.properties
    geometryModifier = context.scene.properties.my_collection_objects.modifiers[props.geometry_modifier_name]
    node_tree = geometryModifier.node_group
    return props, node_tree
    
def update_scattered_obj(self,context):
    props, node_tree = get_object_properties_and_node_tree(context)
    node_tree.nodes['Object Info'].inputs[0].default_value = props.scattered_obj
    
def update_seed(self, context):
    props, node_tree = get_object_properties_and_node_tree(context)
    node_tree.nodes['Distribute Points on Faces'].inputs['Seed'].default_value = props.seed
    
def update_size(self, context):
    props, node_tree = get_object_properties_and_node_tree(context)
    size = (props.size, props.size, props.size)
    node_tree.nodes['Instance on Points'].inputs[6].default_value = size
    
def update_density(self, context):
    props, node_tree = get_object_properties_and_node_tree(context)
    # idk why this node just wants the actual input name 🤔🤔
    node_tree.nodes['Distribute Points on Faces'].inputs['Density'].default_value = props.density

def update_normal_threshold(self, context):
    props, node_tree = get_object_properties_and_node_tree(context)
    node_tree.nodes['Math'].inputs[1].default_value = props.normal_threshold
    
class Object_Properties(PropertyGroup):
    
    scattered_obj: PointerProperty(
        name = "Scattered Object",
        type = bpy.types.Object,
        update = update_scattered_obj
    )
    
    geometry_modifier_name: StringProperty(
        name = "Geometry nodes modifier name",
        description = "used for searching"
    )
    
    seed: IntProperty(
        name = "seed",
        description = "scatter seed",
        default = 0,
        update = update_seed
    )
    
    size: FloatProperty(
        name = "size",
        description = "relative size of scattered objects",
        default = 1,
        min = 0,
        max = 100,
        update = update_size
    )
    
    density: FloatProperty(
        name = "density",
        description = "density of scattered objects",
        default = 1.0,
        min = 0,
        max = 100,
        update = update_density
    )
        
    normal_threshold: FloatProperty(
        name = "normal threshold",
        description = "threshold for dot of normal and object up",
        default = 1.0,
        min = -1,
        max = 1,
        update = update_normal_threshold
    )
