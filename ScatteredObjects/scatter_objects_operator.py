from bpy.types import Operator
import bpy # TODO: maybe import specific thing you need

class OT_ScatterObjects(Operator):
    bl_idname = "operator.scatter_objects"
    bl_label = "Generate"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        scene = context.scene.properties
        base_obj = bpy.context.scene.properties.my_collection_objects
        base_obj_props = base_obj.properties
        density = base_obj_props.density
        normal_threshold = base_obj_props.normal_threshold
        seed = base_obj_props.seed
        
        # initialize geometry nodes modifier
        geo_mod = base_obj.modifiers.new(name="GeometryNodes", type='NODES')
        base_obj_props.geometry_modifier_name = geo_mod.name
        node_tree = bpy.data.node_groups.new("GeometryNodeTree", 'GeometryNodeTree')
        geo_mod.node_group = node_tree
        
        # initialize tree
        node_tree.inputs.new('NodeSocketGeometry', "Inputs")
        node_tree.outputs.new('NodeSocketGeometry', "Outputs")
        
        # initialize nodes
        input_node = node_tree.nodes.new('NodeGroupInput')
        output_node = node_tree.nodes.new('NodeGroupOutput')
        input_node.location.x = -200 - input_node.width
        output_node.location.x = 20
        distribute_points_node = node_tree.nodes.new("GeometryNodeDistributePointsOnFaces")
        distribute_points_node.inputs["Density"].default_value = density
        distribute_points_node.inputs["Seed"].default_value = seed
        object_info_node = node_tree.nodes.new("GeometryNodeObjectInfo")
        object_info_node.inputs[0].default_value = base_obj_props.scattered_obj
        instance_points_node = node_tree.nodes.new("GeometryNodeInstanceOnPoints")
        instance_points_node.inputs[6].default_value = (base_obj_props.size, base_obj_props.size, base_obj_props.size)
        realize_instance_node = node_tree.nodes.new("GeometryNodeRealizeInstances")
        
        vector_node = node_tree.nodes.new("FunctionNodeInputVector")
        vector_node.vector[2] = 1 # set to world up vector
        dot_product_node = node_tree.nodes.new("ShaderNodeVectorMath")
        dot_product_node.operation = 'DOT_PRODUCT'
        subtract_node = node_tree.nodes.new("ShaderNodeMath")
        subtract_node.operation = 'SUBTRACT'
        subtract_node.inputs[1].default_value = base_obj_props.normal_threshold
        
        realize_instance_base_mesh_node = node_tree.nodes.new("GeometryNodeRealizeInstances")
        join_geometry_node = node_tree.nodes.new("GeometryNodeJoinGeometry")
        
        # add links between nodes
        node_tree.links.new(input_node.outputs[0], distribute_points_node.inputs[0])
        node_tree.links.new(object_info_node.outputs[3], instance_points_node.inputs[2])
        node_tree.links.new(distribute_points_node.outputs[0], instance_points_node.inputs[0])
        node_tree.links.new(instance_points_node.outputs[0], realize_instance_node.inputs[0])
        node_tree.links.new(distribute_points_node.outputs[2], instance_points_node.inputs[5])

        node_tree.links.new(distribute_points_node.outputs[1], dot_product_node.inputs[0])
        node_tree.links.new(vector_node.outputs[0], dot_product_node.inputs[1])
        node_tree.links.new(dot_product_node.outputs['Value'], subtract_node.inputs['Value'])
        node_tree.links.new(subtract_node.outputs[0], instance_points_node.inputs[1])
        
        node_tree.links.new(input_node.outputs[0], realize_instance_base_mesh_node.inputs[0])
        node_tree.links.new(realize_instance_base_mesh_node.outputs[0], join_geometry_node.inputs[0])
        node_tree.links.new(realize_instance_node.outputs[0], join_geometry_node.inputs[0])
        node_tree.links.new(join_geometry_node.outputs[0], output_node.inputs[0])
        
        return {'FINISHED'}
