import bpy.types
import logging
from ..pixel_collection import PixelCollection
from ..mesh_evaluators import mesh_evaluator_factory
from ..mesh_evaluators.mesh_evaluator import MeshEvaluator

logger = logging.getLogger(__name__+"."+__file__)


class BakeVat(bpy.types.Operator):
    bl_idname = "object.bake_vertex_animation_texture"
    bl_label = "Bake Vertex Animation Texture"
    bl_options = {'UNDO'}

    def set_image_path_from_index(self, context: bpy.types.Context, image: bpy.types.Image, i: int):
        match i:
            case 0:
                context.scene.vat_export_properties.position_texture_path = image.filepath_raw
            case 1:
                context.scene.vat_export_properties.normal_texture_path = image.filepath_raw
            case 2:
                context.scene.vat_export_properties.tangent_texture_path = image.filepath_raw

    def execute(self, context):
        bake_positions = context.scene.vat_baking_properties.bake_positions
        bake_normals = context.scene.vat_baking_properties.bake_normals
        bake_tangents = context.scene.vat_baking_properties.bake_tangents
        settings_list = [bake_positions, bake_normals, bake_tangents]
        path_list = [context.scene.vat_export_properties.position_texture_path,
                     context.scene.vat_export_properties.normal_texture_path,
                     context.scene.vat_export_properties.tangent_texture_path]

        if not any([bake_positions, bake_normals, bake_tangents]):
            self.report({"WARNING"}, "No bake options selected")
            return {"CANCELLED"}

        object_to_evaluate = context.active_object
        frame_range = (context.scene.vat_baking_properties.frame_start, context.scene.vat_baking_properties.frame_end)
        context.scene.frame_start = frame_range[0]
        context.scene.frame_end = frame_range[1]
        mesh_evaluator = mesh_evaluator_factory.get_mesh_evaluator(context, object_to_evaluate, frame_range)

        context.scene.vat_export_properties.vat_mesh = "NULL"
        context.scene.vat_export_properties.position_texture_path = "NULL"
        context.scene.vat_export_properties.normal_texture_path = "NULL"
        context.scene.vat_export_properties.tangent_texture_path = "NULL"

        name_data = ["POSITION", "NORMAL", "TANGENT"]
        evaluation_functions = [mesh_evaluator.evaluate_position_data, mesh_evaluator.evaluate_normal_data, mesh_evaluator.evaluate_tangent_data]
        for i, setting in enumerate(settings_list):
            if not setting:
                continue
            logger.info(f"Baking VATs for {mesh_evaluator.base_object.name}")
            geometry_data = evaluation_functions[i]()
            logger.info(f"Evaluation function: {evaluation_functions[i]} Geometry Data ({[(px.pixel_data_length(), px.shape) for px in geometry_data]}): {len(geometry_data)}")
            for map_id, image_data in enumerate(geometry_data):
                image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_{name_data[i]}_VAT_{map_id}",
                                            width=image_data.shape[0], height=image_data.shape[1], float_buffer=True,
                                            alpha=True)

                image.pixels = image_data.pixel_data
                image.filepath_raw = f"/tmp/vat_cache/{image.name}.exr"
                self.set_image_path_from_index(context, image, i)
                image.file_format = 'OPEN_EXR'
                image.save()

        if any([bake_positions, bake_normals, bake_tangents]):
            context.scene.vat_export_properties.vat_mesh = mesh_evaluator.base_object.name

        return {"FINISHED"}


def register():
    from bpy.utils import register_class
    try:
        register_class(BakeVat)
    except:
        pass


def unregister():
    from bpy.utils import unregister_class

    try:
        unregister_class(BakeVat)
    except:
        pass