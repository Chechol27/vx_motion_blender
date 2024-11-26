import bpy
from bpy.types import Panel


class VXMotionPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VXMotion"


class BakeVATMenu(Panel, VXMotionPanel):
    bl_label = "Bake Vertex Animation Textures"

    def draw(self, context: bpy.types.Context):
        pass


class BakeVATOptionsMenu(Panel, VXMotionPanel):
    bl_label = "Baking Options"
    bl_parent_id = "BakeVATMenu"

    def draw(self, context: bpy.types.Context):
        scene = context.scene

        layout = self.layout
        layout.prop(scene.vat_baking_properties, "frame_start", text="Start Frame")
        layout.prop(scene.vat_baking_properties, "frame_end", text="End Frame")
        layout.prop(scene.vat_baking_properties, "bake_positions", text="Bake Positions")
        layout.prop(scene.vat_baking_properties, "bake_normals", text="Bake Normals")
        layout.prop(scene.vat_baking_properties, "bake_tangents", text="Bake Tangents")
        layout.operator("object.bake_vertex_animation_texture", text="Bake VATs")


class ExportVatMenu(Panel, VXMotionPanel):
    bl_label = "Export Vertex Animation Textures"

    def draw(self, context):
        pass


class ExportVatOptionsMenu(Panel, VXMotionPanel):
    bl_label = "Export Options"
    bl_parent_id = "ExportVatMenu"

    def draw(self, context: bpy.types.Context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene.vat_export_properties, "export_path", text="Exoport path")
        layout.operator("object.export_vertex_animattion_textures", text="Export VATs")


def register():
    from bpy.utils import register_class
    try:
        register_class(BakeVATMenu)
        register_class(BakeVATOptionsMenu)
        register_class(ExportVatMenu)
        register_class(ExportVatOptionsMenu)
    except:
        pass


def unregister():
    from bpy.utils import unregister_class

    try:
        unregister_class(ExportVatOptionsMenu)
        unregister_class(ExportVatMenu)
        unregister_class(BakeVATOptionsMenu)
        unregister_class(BakeVATMenu)
    except:
        pass

