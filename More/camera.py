bl_info = {
    "name": "test_zuuuuuuuuu",
    "author": "alonzu",
    "description": "test addon",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

import bpy
camera_object = None


class MyProperties(bpy.types.PropertyGroup):
    camera_distance: bpy.props.FloatProperty(
        name="Camera Distance",
        default=5.0,
        min=1,
        max=100.0,
        step=0.5,
        description="Distance of the camera from the center of the scene",
        update=lambda self, context: update_camera_location(context.scene)
    )


class MyPanel(bpy.types.Panel):
    bl_label = "Camera Settings"
    bl_idname = "OBJECT_PT_my_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My Panel"

    def draw(self, context):
        # UI setup
        layout = self.layout

        # Camera UI
        layout.label(text="Camera")
        row = layout.row()
        layout.operator("object.add_camera")
        layout.prop(context.scene.my_properties, "camera_distance")

        layout.label(text="Add")
        layout = self.layout
        layout.prop(context.scene, "cubes_count")
        layout.operator("object.add_cubes", text="Add Cubes")


class AddCameraOperator(bpy.types.Operator):
    bl_idname = "object.add_camera"
    bl_label = "Add Camera"

    def execute(self, context):
        global camera_object
        if camera_object is not None:
            return {'FINISHED'}

        # Create a new camera object
        camera_data = bpy.data.cameras.new(name='Camera')
        camera_object = bpy.data.objects.new(name='Camera', object_data=camera_data)
        context.scene.collection.objects.link(camera_object)
        context.scene.camera = camera_object

        target_object = bpy.data.objects.new(name='Target', object_data=None)
        target_object.location = (0, 0, 0)
        context.scene.collection.objects.link(target_object)

        # Add a track-to constraint to the camera to make it point at the target object
        track_constraint = camera_object.constraints.new('TRACK_TO')
        track_constraint.target = target_object
        track_constraint.up_axis = 'UP_Y'
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'

        # Split the 3D View area and create a new one
        areas = bpy.context.screen.areas
        for area in areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.screen.area_split(override, direction='VERTICAL', factor=0.5)
                break

        # Set the new area's space to 3D View
        for area in areas:
            if area.type == 'VIEW_3D' and area != context.area:
                new_area = area
                break
        new_area.spaces[0].region_3d.view_perspective = 'CAMERA'


        # Set UI panel off
        override = bpy.context.copy()
        override['area'] = new_area
        override['space_data'] = new_area.spaces.active
        bpy.ops.wm.context_toggle(override, data_path="space_data.show_region_ui")

        # Set the camera location based on the camera distance property
        update_camera_location(context.scene)

        return {'FINISHED'}


def update_camera_location(scene):
    # Set the camera location based on the camera distance property
    camera_distance = scene.my_properties.camera_distance
    camera_object = scene.camera
    if camera_object is not None:
        camera_object.location = (camera_distance, camera_distance, camera_distance)


class OBJECT_OT_AddCubesOperator(bpy.types.Operator):
    bl_label = "Add Cubes"
    bl_idname = "object.add_cubes"

    def execute(self, context):
        cubes_count = context.scene.cubes_count
        for i in range(cubes_count):
            bpy.ops.mesh.primitive_cube_add(location=(i, 0, 0))
        return {'FINISHED'}


def register():
    bpy.types.Scene.cubes_count = bpy.props.IntProperty(
        name="Cubes Count",
        description="Number of cubes",
        default=1,
        min=1
    )
    bpy.utils.register_class(OBJECT_OT_AddCubesOperator)

    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.my_properties = bpy.props.PointerProperty(type=MyProperties)
    bpy.utils.register_class(MyPanel)
    bpy.utils.register_class(AddCameraOperator)
    bpy.app.handlers.scene_update_post.append(update_camera_location)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_AddCubesOperator)
    del bpy.types.Scene.cubes_count


    bpy.utils.unregister_class(MyProperties)
    del bpy.types.Scene.my_properties
    bpy.utils.unregister_class(MyPanel)
    bpy.utils.unregister_class(AddCameraOperator)
    bpy.app.handlers.scene_update_post.remove(update_camera_location)


if __name__ == "__main__":
    register()


