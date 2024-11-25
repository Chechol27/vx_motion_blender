import bpy.types
import numpy
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
        tangent_data = mesh_evaluator.evaluate_tangent_data()

        #TODO: Create images, export as exr, trigger subprocess for previsualization using vulkan mini app
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