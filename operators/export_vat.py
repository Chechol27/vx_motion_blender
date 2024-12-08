import bpy
import os
from zipfile import ZipFile

class ExportVat(bpy.types.Operator):
    bl_idname = "object.export_vertex_animation_textures"
    bl_label = "Export Vertex Animation Textures"
    bl_options = {'UNDO'}

    def assert_export_textures(self, scene: bpy.types.Scene):
        texture_paths = [scene.vat_export_properties.position_texture_path, scene.vat_export_properties.normal_texture_path, scene.vat_export_properties.tangent_texture_path]
        textures_exist = any([os.path.exists(path) for path in texture_paths])
        non_null_paths = [path for path in texture_paths if path != "NULL"]
        object_exists = bpy.data.objects.get(scene.vat_export_properties.vat_mesh)
        textures_match = all([scene.vat_export_properties.vat_mesh in path for path in non_null_paths])
        return textures_exist and object_exists and textures_match

    def execute(self, context):
        scene = context.scene
        if not self.assert_export_textures(scene):
            self.report({'WARNING'}, "Baking data corrupted, try to re bake or check if any of the require data was not eliminated")
            return {'CANCELLED'}
        texture_paths = [scene.vat_export_properties.position_texture_path, scene.vat_export_properties.normal_texture_path, scene.vat_export_properties.tangent_texture_path]
        non_null_paths = [path for path in texture_paths if path != "NULL"]
        mesh_object = bpy.data.objects.get(scene.vat_export_properties.vat_mesh)
        bpy.ops.object.select_all(action="DESELECT")
        mesh_object.select_set(True)
        mesh_path = f"C:/tmp/vat_cache/{mesh_object.name}.obj"
        bpy.ops.wm.obj_export(filepath=mesh_path, export_selected_objects=True)

        export_path = scene.vat_export_properties.export_path
        export_data = []
        for f in os.listdir(r"C:\tmp\vat_cache"):
            export_data.append(os.path.join(r"C:\tmp\vat_cache", f))
        for file in export_data:
            print(file)
        with ZipFile(os.path.join(export_path, mesh_object.name+".vatclip"), "w") as zip:
            for file in export_data:
                zip.write(file, arcname=os.path.basename(file))

        return {'FINISHED'}


def register():
    from bpy.utils import register_class
    try:
        register_class(ExportVat)
    except:
        pass


def unregister():
    from bpy.utils import unregister_class

    try:
        unregister_class(ExportVat)
    except:
        pass