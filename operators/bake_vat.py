import bpy.types
import numpy
from ..pixel_collection import PixelCollection
from ..mesh_evaluators import mesh_evaluator_factory
from ..mesh_evaluators.mesh_evaluator import MeshEvaluator

class BakeVat(bpy.types.Operator):
    bl_idname = "object.bake_vertex_animation_texture"
    bl_label = "Bake Vertex Animation Texture"
    bl_options = {'UNDO'}

    def execute(self, context):

        bake_positions = context.scene.vat_baking_properties.bake_positions
        bake_normals = context.scene.vat_baking_properties.bake_normals
        bake_tangents = context.scene.vat_baking_properties.bake_tangents

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
        for i, setting in enumerate([bake_positions, bake_normals, bake_tangents]):
            if not setting:
                continue
            geometry_data = evaluation_functions[i]()
            for map_id, image_data in enumerate(geometry_data):
                image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_{name_data[i]}_VAT_{map_id}",
                                            width=image_data.shape[0], height=image_data.shape[1], float_buffer=True,
                                            alpha=False)
                image.pixels = image_data.pixel_data
                image.filepath_raw = f"C:/tmp/vat_cache/{image.name}.exr"
                match i:
                    case 0:
                        context.scene.vat_export_properties.position_texture_path = image.filepath_raw
                    case 1:
                        context.scene.vat_export_properties.normal_texture_path = image.filepath_raw
                    case 2:
                        context.scene.vat_export_properties.tangent_texture_path = image.filepath_raw
                image.file_format = 'OPEN_EXR'
                image.save()


        # counter = 0
        # if context.scene.vat_baking_properties.bake_positions:
        #     counter += 1
        #     position_data = mesh_evaluator.evaluate_position_data()
        #     for map_id, image_data in enumerate(position_data):
        #         image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_POSITION_VAT_{map_id}", width=image_data.shape[0], height=image_data.shape[1], float_buffer=True, alpha=False)
        #         image.pixels = image_data.pixel_data
        #         image.filepath_raw = f"C:/tmp/{image.name}.exr"
        #         context.scene.vat_export_properties.position_texture_path = image.filepath_raw
        #         image.file_format = 'OPEN_EXR'
        #         image.save()
        #
        # if context.scene.vat_baking_properties.bake_normals:
        #     counter += 1
        #     normal_data = mesh_evaluator.evaluate_normal_data()
        #     for map_id, image_data in enumerate(normal_data):
        #         image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_NORMAL_VAT_{map_id}", width=image_data.shape[0], height=image_data.shape[1], float_buffer=True, alpha=False)
        #         image.pixels = image_data.pixel_data
        #         image.filepath_raw = f"C:/tmp/{image.name}.exr"
        #         context.scene.vat_export_properties.normal_texture_path = image.filepath_raw
        #         image.file_format = 'OPEN_EXR'
        #         image.save()
        #
        # if context.scene.vat_baking_properties.bake_tangents:
        #     counter += 1
        #     tangent_data = mesh_evaluator.evaluate_tangent_data()
        #     for map_id, image_data in enumerate(tangent_data):
        #         image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_TANGENT_VAT_{map_id}", width=image_data.shape[0], height=image_data.shape[1], float_buffer=True, alpha=False)
        #         image.pixels = image_data.pixel_data
        #         image.filepath_raw = f"C:/tmp/{image.name}.exr"
        #         context.scene.vat_export_properties.tangent_texture_path = image.filepath_raw
        #         image.file_format = 'OPEN_EXR'
        #         image.save()

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