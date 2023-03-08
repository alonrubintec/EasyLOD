import bpy
import math
import os

bl_info = {
    "name": "EasyLOD",
    "author": "Alon Rubin",
    "description": "Easy LOD Maker",
    "blender": (3, 00, 0),
    "location": "View3D > Tools Panel > My Addon",
    "warning": "",
    "category": "Easy"
}

ui_space = 0.35
version = 1.1


class PanelClass:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Easy LOD"


class MainPanel(PanelClass, bpy.types.Panel):
    bl_idname = "MainPanel"
    bl_label = f"Easy LOD - v{version}"

    def draw(self, context):
        layout = self.layout
        split = layout.split(factor=1.0)
        col1 = split.column(align=True)
        col1.alignment = 'LEFT'
        col1.label(text="     by Alon Rubin")


class Settings_Panel(PanelClass, bpy.types.Panel):
    bl_parent_id = "MainPanel"
    bl_label = "Settings"

    def draw(self, context):
        layout = self.layout

        split = layout.split(factor=ui_space)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=True)
        col2.alignment = 'RIGHT'
        col1.label(text="Amount")
        col2.prop(context.scene, "num_modifiers", slider=True)

        split2 = layout.split(factor=ui_space)
        col3 = split2.column(align=True)
        col3.alignment = 'RIGHT'
        col4 = split2.column(align=True)
        col4.alignment = 'RIGHT'
        col3.label(text="Intensity")
        col4.prop(context.scene, "intensity", slider=True)

        split4 = layout.split(factor=ui_space)
        col7 = split4.column(align=True)
        col7.alignment = 'RIGHT'
        col8 = split4.column(align=True)
        col8.alignment = 'RIGHT'
        col7.label(text="Ratio")
        col8.prop(context.scene, "ratio_power", slider=True)

        layout.separator()

        split3 = layout.split(factor=ui_space)
        col5 = split3.column(align=True)
        col5.alignment = 'RIGHT'
        col6 = split3.column()
        col5.label(text="Symmetry")
        col6.prop(context.scene, "symmetry")


class Start_Panel(PanelClass, bpy.types.Panel):
    bl_parent_id = "MainPanel"
    bl_label = "LOD group"

    def draw(self, context):
        layout = self.layout

        split = layout.split(factor=ui_space)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=True)
        col2.alignment = 'RIGHT'
        col1.label(text="")
        col2.operator("object.add_decimate_modifier")

        split2 = layout.split(factor=ui_space)
        col3 = split2.column(align=True)
        col3.alignment = 'RIGHT'
        col4 = split2.column(align=True)
        col4.alignment = 'RIGHT'
        col3.label(text="")
        col4.operator("object.remove_modifiers")

        split3 = layout.split(factor=ui_space)
        col5 = split3.column(align=True)
        col5.alignment = 'RIGHT'
        col6 = split3.column(align=True)
        col6.alignment = 'RIGHT'
        col5.label(text=f"{context.scene.current_modifier}")
        col6.prop(context.scene, "visibility", slider=True)


    def update_visibility(self, context):

        # Get the maximum number of modifiers
        max_modifiers = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH' and len(obj.modifiers) > max_modifiers:
                max_modifiers = len(obj.modifiers)

        # Normalize the ui slider to the number of modifiers
        visibility_percent = context.scene.visibility / 100
        modifier_index = round(visibility_percent * (max_modifiers - 1))

        # Set the visibility of the modifiers
        current_modifier = None
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                for i, mod in enumerate(obj.modifiers):
                    if i == modifier_index:
                        mod.show_viewport = True
                        current_modifier = mod.name
                    else:
                        mod.show_viewport = False

        # Set the current_modifier property of the scene to the name of the current modifier
        if current_modifier:
            context.scene.current_modifier = current_modifier
        else:
            context.scene.current_modifier = ""

    # Register the update function as a handler for the visibility property
    bpy.types.Scene.visibility = bpy.props.IntProperty(
        name="",
        default=0,
        min=0,
        max=100,
        description="Visibility of the active LOD",
        update=update_visibility
    )


class Export_Panel(PanelClass, bpy.types.Panel):
    bl_parent_id = "MainPanel"
    bl_label = "Export"

    def draw(self, context):
        layout = self.layout

        layout.separator()

        split = layout.split(factor=ui_space)
        col1 = split.column(align=True)
        col1.alignment = 'RIGHT'
        col2 = split.column(align=True)
        col2.alignment = 'RIGHT'
        col1.label(text="Path")
        col2.prop(context.scene, "export_fbx_path")

        split2 = layout.split(factor=ui_space)
        col3 = split2.column(align=True)
        col3.alignment = 'RIGHT'
        col4 = split2.column(align=True)
        col4.alignment = 'RIGHT'
        col3.label(text="Export")
        col4.operator("object.export", text="Export FBX")

        layout.separator()


class ExportLODs(bpy.types.Operator):
    bl_idname = "object.export"
    bl_label = "Copy Object with Decimate Modifiers"

    def execute(self, context):

        if context.scene.export_fbx_path == "":
            ShowMessageBox("No path to export!")
            return {'FINISHED'}

        # Check if any object selected
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) < 1:
            ShowMessageBox("No object selected to export!")
            return {'FINISHED'}

        # Check if there are modifier
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            decimate_modifiers_objects = [modifier for modifier in obj.modifiers if modifier.type == 'DECIMATE']
            if not decimate_modifiers_objects:
                ShowMessageBox("NO LOD: Add LOD group", "ERROR", "ERROR")
                return {'FINISHED'}

        # Create collections with new models
        collection_list = []
        for current_object in selected_objects:
            selected_object = current_object
            decimate_modifiers = [modifier for modifier in selected_object.modifiers if modifier.type == 'DECIMATE']
            Export_collection = bpy.data.collections.new(name=selected_object.name)
            collection_list.append(Export_collection)

            # Create new models
            for modifier in decimate_modifiers:
                copied_object = selected_object.copy()
                copied_object.data = selected_object.data.copy()
                copied_object.modifiers.clear()

                decimate_modifier = copied_object.modifiers.new(name=modifier.name, type='DECIMATE')
                decimate_modifier.ratio = modifier.ratio
                copied_object.name = f"{selected_object.name}_{modifier.name}"

                Export_collection.objects.link(copied_object)

            # Deselect the original object
            selected_object.select_set(False)
            context.scene.collection.children.link(Export_collection)

            # Apply Modifiers
            for object in Export_collection.objects:
                object.select_set(True)
                bpy.context.view_layer.objects.active = object
                bpy.ops.object.modifier_apply(modifier=modifier.name)

        # Deselect all objects in the scene
        bpy.ops.object.select_all(action='DESELECT')

        # Get and clean path
        export_path = context.scene.export_fbx_path
        base_path, extension = os.path.splitext(export_path)
        if extension:
            export_path = base_path

        for export_collection in collection_list:
            temp_path = export_path

            temp_path += export_collection.name
            temp_path += '.fbx'

            # Select all objects in the collection
            for obj in export_collection.objects:
                obj.select_set(True)

            # Export
            bpy.ops.export_scene.fbx(filepath=temp_path, use_selection=True)
            for obj in export_collection.objects:
                export_collection.objects.unlink(obj)
                bpy.data.objects.remove(obj)

        # Delete the collection
        for delete_collection in collection_list:
            bpy.data.collections.remove(delete_collection)
        return {'FINISHED'}


class AddModifier(bpy.types.Operator):
    bl_idname = "object.add_decimate_modifier"
    bl_label = "Add"
    bl_description = "Add LODs to Selected Objects"


    def execute(self, context):
        selected_objects = context.selected_objects

        if len(selected_objects) < 1:
            ShowMessageBox("No object selected!")
            return {'FINISHED'}

        context.scene.visibility = 100
        # Check if object has Decimate Modifier
        for obj in selected_objects:
            if obj.type == 'MESH':
                has_decimate_modifier = False
                for modifier in obj.modifiers:
                    if modifier.type == 'DECIMATE':
                        has_decimate_modifier = True
                        break
                if has_decimate_modifier:
                    return {'FINISHED'}

        num_modifiers = context.scene.num_modifiers
        ratio_power = context.scene.ratio_power
        intensity = context.scene.intensity

        # Invert intensity
        intensity = 100 - intensity

        # Map intensity to logarithmic scale between 0.001 and 0.1
        ratio_intensity = 5
        intensity = math.exp((intensity - 1) * ratio_intensity / 99.0 - ratio_intensity) / 10.0 + 0.001

        for obj in selected_objects:
            if obj.type == 'MESH':
                for i in range(num_modifiers):
                    mod = obj.modifiers.new(name=f"LOD{i}", type='DECIMATE')
                    mod.show_expanded = False
                    mod.show_viewport = False

                    # Use logarithmic scale to set modifier ratio
                    ratio = (num_modifiers - i - 1) / (num_modifiers - 1)
                    ratio = math.exp(ratio * ratio_power) / math.exp(ratio_power)
                    mod.ratio = intensity + (1 - intensity) * ratio

                    if i == num_modifiers - 1:
                        mod.show_expanded = True
                        mod.show_viewport = True

                    # Check the value of the symmetry property
                    scene = bpy.context.scene
                    if scene.symmetry:
                        mod.use_symmetry = True

                    context.scene.current_modifier = mod.name

        return {'FINISHED'}


class RemoveModifier(bpy.types.Operator):
    bl_idname = "object.remove_modifiers"
    bl_label = "Remove"
    bl_description = "Remove all decimate modifiers from selected objects"

    def execute(self, context):
        selected_objects = context.selected_objects

        if len(selected_objects) < 1:
            ShowMessageBox("No object selected!")
            return {'FINISHED'}

        context.scene.visibility = -1

        context.scene.current_modifier = ""
        for obj in selected_objects:
            if obj.type == 'MESH':
                for mod in obj.modifiers:
                    if mod.type == 'DECIMATE':
                        obj.modifiers.remove(mod)

        return {'FINISHED'}


bpy.types.Scene.num_modifiers = bpy.props.IntProperty(
    name="",
    default=6,
    min=2,
    max=10,
    description="Number of decimate modifiers to add"
)

bpy.types.Scene.ratio_power = bpy.props.FloatProperty(
    name="",
    default=3.95,
    min=2,
    max=6,
    description="Ratio",
    precision=1
)



def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


Classes = (MainPanel, Settings_Panel, Start_Panel, Export_Panel,
           AddModifier, RemoveModifier, ExportLODs)


def register():
    update_visibility = None
    # Classes
    for c in Classes:
        bpy.utils.register_class(c)

    # Property
    bpy.types.Scene.current_modifier = bpy.props.StringProperty()
    bpy.types.Scene.intensity = bpy.props.IntProperty(
        name="",
        default=50,
        min=1,
        max=100,
        description="Intensity for the decimate modifier ratio"
    )
    bpy.types.Scene.symmetry = bpy.props.BoolProperty(
        name="",
        description="Toggle symmetry",
        default=False
    )
    bpy.types.Scene.export_fbx_path = bpy.props.StringProperty(
        name="",
        subtype="FILE_PATH",
        default=""
    )
    bpy.types.Scene.visibility = bpy.props.IntProperty(
        name="",
        default=0,
        min=0,
        max=100,
        description="Visibility of the active LOD",
        update=update_visibility
    )

def unregister():

    # Classes
    for c in Classes:
        bpy.utils.unregister_class(c)

    # Property
    del bpy.types.Scene.visibility
    del bpy.types.Scene.intensity
    del bpy.types.Scene.symmetry
    del bpy.types.Scene.current_modifier
    del bpy.types.Scene.export_fbx_path


if __name__ == "__main__":
    register()
