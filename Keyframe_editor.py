import bpy

def get_selected_keyframes():
    obj = bpy.context.object
    selected_keyframes = []
    if obj and obj.animation_data and obj.animation_data.action:
        fcurves = obj.animation_data.action.fcurves
        for fcurve in fcurves:
            for keyframe in fcurve.keyframe_points:
                if keyframe.select_control_point:
                    selected_keyframes.append((fcurve, keyframe))
    return selected_keyframes

class GRAPH_OT_EditKeyframes(bpy.types.Operator):
    bl_idname = "graph.edit_keyframes"
    bl_label = "Edit Keyframes"

    value: bpy.props.FloatProperty(name="Value")

    def execute(self, context):
        selected_keyframes = get_selected_keyframes()
        if selected_keyframes:
            for fcurve, keyframe in selected_keyframes:
                keyframe.co.y = self.value
                fcurve.update()
            context.area.tag_redraw()
        return {'FINISHED'}

class GRAPH_PT_KeyframeEditor(bpy.types.Panel):
    bl_label = "Raha Keyframe Editor"
    bl_idname = "GRAPH_PT_keyframe_editor"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Raha Keyframe Editor'

    def draw(self, context):
        layout = self.layout
        selected_keyframes = get_selected_keyframes()
        
        layout.label(text="Edit Value") 
        if selected_keyframes:
            last_fcurve, last_keyframe = selected_keyframes[-1]
            layout.label(text=f"Frame: {last_keyframe.co.x:.2f}")
            layout.prop(last_keyframe, "co", text="Value", index=1)
            op = layout.operator("graph.edit_keyframes", text="Apply to selected")
            op.value = last_keyframe.co.y
        else:
            layout.label(text="No keyframe selected")
            
        layout.label(text="Animation Cycles")           
        layout = self.layout
        layout.operator("anim.add_cycles", text="Add Cycles")
        layout.operator("anim.remove_cycles", text="Delete Cycles")
        layout.separator()
        layout.label(text="Set Cycles Mode")
        col = layout.column()
        col.operator_menu_enum("anim.set_cycles_mode", "mode", text="Before Mode").before = True
        col.operator_menu_enum("anim.set_cycles_mode", "mode", text="After Mode").before = False
    

def register():
    bpy.utils.register_class(GRAPH_OT_EditKeyframes)
    bpy.utils.register_class(GRAPH_PT_KeyframeEditor)

def unregister():
    bpy.utils.unregister_class(GRAPH_OT_EditKeyframes)
    bpy.utils.unregister_class(GRAPH_PT_KeyframeEditor)

if __name__ == "__main__":
    register()
