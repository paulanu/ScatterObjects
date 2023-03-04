from bpy.types import Panel

class PT_ScatterObjects(Panel):
    bl_idname = "PT_ScatterObjects"
    bl_label = "Scatter Objects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        col = layout.column()
        col.prop(scene.properties, "my_collection")
        
        col = layout.column()
        col.enabled = True if scene.properties.my_collection else False
        col.prop(scene.properties, "my_collection_objects")
                
        base_obj = scene.properties.my_collection_objects;
        
        #TODO: find a way of enabling/disabling these items instead of just not displaying them at all
        if (base_obj is not None):
            # TODO: make sure to prevent the base obj from appearing in the scattered objects list
            col = layout.column()
            col.prop(base_obj.properties, "scattered_obj")
            
            col = layout.column()
            col.prop(base_obj.properties, "seed")
            
            col = layout.column()
            col.prop(base_obj.properties, "size")
            
            col = layout.column()
            col.prop(base_obj.properties, "density")

            col = layout.column()
            col.prop(base_obj.properties, "normal_threshold")
            
            if (base_obj.properties.scattered_obj is not None):
                if (base_obj.modifiers.find(base_obj.properties.geometry_modifier_name) == -1):
                    scatterop = self.layout.operator('operator.scatter_objects')
                else:
                    applyop = self.layout.operator('operator.apply_scatter')
