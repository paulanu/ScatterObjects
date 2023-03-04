from bpy.types import Operator
import bpy # TODO: maybe import specific thing you need
import numpy as np
import mathutils

# TODO: does using 2 operators make sense for generate/apply?
# TODO: look up difference btwn invoke and execute (which one is used when)
class OT_ApplyScatter(Operator):
    bl_idname = "operator.apply_scatter"
    bl_label = "Apply"
    bl_options = {'REGISTER', 'UNDO'}
      
    def execute(self, context):
        base_obj = bpy.context.scene.properties.my_collection_objects
        scene = bpy.context.scene
        geometry_modifier = base_obj.modifiers[base_obj.properties.geometry_modifier_name]
        node_tree = geometry_modifier.node_group
        
        # adjust geometry modifier so it is only outputting points
        instance_points_node = node_tree.nodes['Instance on Points']
        realize_instance_node = node_tree.nodes['Realize Instances']
        distribute_points_node = node_tree.nodes['Distribute Points on Faces']
        output_node = node_tree.nodes['Group Output']
        mesh_line_node = node_tree.nodes.new("GeometryNodeMeshLine")
        mesh_line_node.inputs[0].default_value = 1
        
        node_tree.links.new(mesh_line_node.outputs[0], instance_points_node.inputs[2])
        node_tree.links.new(realize_instance_node.outputs[0], output_node.inputs[0])

        # read point values from graph
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj = base_obj.evaluated_get(depsgraph)
        coords = np.zeros(len(obj.data.vertices) * 3, dtype=float)
        obj.data.vertices.foreach_get("co", coords)
        coords = coords.reshape(len(obj.data.vertices), 3)

        # translate points along normal in geometry node
        # I found no other way to get normal point data from the modifier - the actual points do not have correct normals/orientation
        translate_instances_node = node_tree.nodes.new("GeometryNodeTranslateInstances")
        node_tree.links.new(instance_points_node.outputs[0], translate_instances_node.inputs[0])
        node_tree.links.new(translate_instances_node.outputs[0], realize_instance_node.inputs[0])
        node_tree.links.new(distribute_points_node.outputs[1], translate_instances_node.inputs[2]) # normal translation
        
        # grab translation
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj = base_obj.evaluated_get(depsgraph)
        normals = np.zeros(len(obj.data.vertices) * 3, dtype=float)
        obj.data.vertices.foreach_get("co", normals)
        normals = normals.reshape(len(obj.data.vertices), 3)
    
        # remove modifier, no more use for it now
        base_obj.modifiers.remove(geometry_modifier)

        # create collection for scattered objs and set as active
        scattered_objs_collection = bpy.data.collections.new("ScatteredObjects")
        bpy.context.scene.collection.children.link(scattered_objs_collection)
        layer_collection = bpy.context.view_layer.layer_collection.children[scattered_objs_collection.name]
        bpy.context.view_layer.active_layer_collection = layer_collection

        # instantiate scattered objs
        for point, normalcalc in zip(coords, normals):
            rock = base_obj.properties.scattered_obj.copy()
            rock.data = rock.data.copy()
            bpy.context.view_layer.active_layer_collection.collection.objects.link(rock)
          
            # convert local points to world space
            mat_objtoworld = base_obj.matrix_world
            point_local = mat_objtoworld @ mathutils.Vector((point[0], point[1], point[2]))
            normal_local = mat_objtoworld @ mathutils.Vector((normalcalc[0], normalcalc[1], normalcalc[2]))
            normal_local = normal_local - point_local
            normal_local.normalize()
            
            # normal cutoff
            if (normal_local.dot(mathutils.Vector((0.0, 0.0, 1.0))) < base_obj.properties.normal_threshold):
                continue
            
            rock.location = point_local
            rock.scale *= base_obj.properties.size
            #TODO: This math is wrong, redo calculation method!!!
            rock.rotation_mode = 'QUATERNION'
            rock.rotation_quaternion = normal_local.to_track_quat('Z','Y')
        return {'FINISHED'}
