bl_info = {
    "name": "Add Camera Rigged",
    "author": "Netherby",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "Add > Camera > Camera Rigged",
    "description": "Adds a camera with a tracking empty",
    "category": "Add Camera",
}

import bpy
from mathutils import Vector

class OBJECT_OT_add_camera_rigged(bpy.types.Operator):
    """Add a camera with a tracking empty"""
    bl_idname = "object.add_camera_rigged"
    bl_label = "Camera Rigged"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Add a standard camera using Blender's built-in operator
        bpy.ops.object.camera_add()
        cam = context.active_object

        # Create the focus empty
        empty = bpy.data.objects.new(f"{cam.name}.focus", None)
        empty.empty_display_type = 'SPHERE'
        context.collection.objects.link(empty)

        # Position the empty in front of the camera
        # (roughly where the camera is looking)
        empty.location = cam.location + cam.matrix_world.to_quaternion() @ Vector((0, 0, -5))

        # Add Damped Track constraint to the camera
        constraint = cam.constraints.new(type="DAMPED_TRACK")
        constraint.target = empty
        constraint.track_axis = 'TRACK_NEGATIVE_Z'

        return {'FINISHED'}


# --- Menu code ---

def menu_func(self, context):
    self.layout.operator(
        OBJECT_OT_add_camera_rigged.bl_idname,
        text="Camera Rigged",
        icon='CAMERA_DATA'
    )


def register():
    bpy.utils.register_class(OBJECT_OT_add_camera_rigged)
    bpy.types.VIEW3D_MT_camera_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_camera_add.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_add_camera_rigged)


if __name__ == "__main__":
    register()