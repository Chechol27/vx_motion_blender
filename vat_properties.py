
import bpy

class VatBakingProperties(bpy.types.PropertyGroup):
    frame_start: bpy.props.IntProperty(name="Frame Start")
    frame_end: bpy.props.IntProperty(name="Frame End")
    bake_positions: bpy.props.BoolProperty(name="Bake Positions")
    bake_normals: bpy.props.BoolProperty(name="Bake Positions")
    bake_tangents: bpy.props.BoolProperty(name="Bake Positions")


class VatExportProperties(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(name="Export Path")
    vat_mesh: bpy.props.StringProperty(name="Vat Mesh")
    position_texture_path: bpy.props.StringProperty(name="Position Texture")
    normal_texture_path: bpy.props.StringProperty(name="Normal Texture")
    tangent_texture_path: bpy.props.StringProperty(name="Tangent Texture")


def register():
    from bpy.utils import register_class
    try:
        register_class(VatBakingProperties)
        register_class(VatExportProperties)
        bpy.types.Scene.vat_baking_properties = bpy.props.PointerProperty(type=VatBakingProperties)
        bpy.types.Scene.vat_export_properties = bpy.props.PointerProperty(type=VatExportProperties)
    except:
        pass


def unregister():
    from bpy.utils import unregister_class

    try:
        unregister_class(VatExportProperties)
        unregister_class(VatBakingProperties)
    except:
        pass