import bpy
import math
import os

bl_info = {
    "name": "Easy LOD",
    "author": "Alon Rubin",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Easy LOD",
    "category": "Object",
}
ui_space = 0.3


class PanelClass:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Easy LOD"


class MainPanel(PanelClass, bpy.types.Panel):
    bl_idname = "MainPanel"
    bl_label = "Main"

    def draw(self, context):
        pass


class Settings_Panel(PanelClass, bpy.types.Panel):
    bl_parent_id = "MainPanel"
    bl_label = "Settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Settings_Panel")


class Start_Panel(PanelClass, bpy.types.Panel):
    bl_parent_id = "MainPanel"
    bl_label = "Start"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Start_Panel")

class Export_Panel(PanelClass, bpy.types.Panel):
    bl_parent_id = "MainPanel"
    bl_label = "Export"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Export_Panel")


Panel_classes = (MainPanel, Settings_Panel, Start_Panel, Export_Panel)


def register():
    for cls in Panel_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in Panel_classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()