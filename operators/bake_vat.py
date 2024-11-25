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
        self.report({"INFO"}, "Should bake VAT")
        object_to_evaluate = context.active_object
        frame_range = (1, 64)
        mesh_evaluator = mesh_evaluator_factory.get_mesh_evaluator(context, object_to_evaluate, frame_range)
        position_data = mesh_evaluator.evaluate_position_data()
        normal_data = mesh_evaluator.evaluate_normal_data()
        #tangent_data = mesh_evaluator.evaluate_tangent_data()

        #TODO: Create images, export as exr, trigger subprocess for previsualization using vulkan mini app
        for map_id, image_data in enumerate(position_data):
            image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_POSITION_VAT_{map_id}", width=image_data.shape[0], height=image_data.shape[1], float_buffer=True, alpha=False)
            image.pixels = image_data.pixel_data
            image.filepath_raw = f"/tmp/{image.name}.exr"
            image.file_format = 'OPEN_EXR'
            image.save()

        for map_id, image_data in enumerate(normal_data):
            image = bpy.data.images.new(f"{mesh_evaluator.base_object.name}_NORMAL_VAT_{map_id}", width=image_data.shape[0], height=image_data.shape[1], float_buffer=True, alpha=False)
            image.pixels = image_data.pixel_data
            image.filepath_raw = f"/tmp/{image.name}.exr"
            image.file_format = 'OPEN_EXR'
            image.save()

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