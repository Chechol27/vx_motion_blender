import math
import bpy
import bmesh
import numpy
import numpy as np

from .mesh_evaluator import MeshEvaluator
from mathutils import Vector
from ..pixel_collection import PixelCollection


class ConstantTopologyEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection from an object which animation has a constant topology
    useful for rigged meshes , soft bodies, ocean, clothes, etc
    """
    evaluated_meshes: [bpy.types.Mesh] = []
    object_to_evaluate: bpy.types.Object = None
    uv_layers: list[tuple[int, bpy.types.MeshUVLoopLayer]]
    base_object: bpy.types.Object
    frame_range: (int, int)

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)
        self.frame_range = frame_range
        self.evaluated_meshes = []
        self.object_to_evaluate = object_to_evaluate
        self.uv_layers = []
        for i in range(self.frame_range[0], self.frame_range[1] + 1):
            context.scene.frame_set(i)
            deps_graph = context.evaluated_depsgraph_get()
            eval_obj = object_to_evaluate.evaluated_get(deps_graph)
            self.evaluated_meshes.append(bpy.data.meshes.new_from_object(eval_obj))
            if i == self.frame_range[0]:
                self.create_base_object(context)

    def create_base_object(self, context: bpy.types.Context):
        mesh = self.evaluated_meshes[0]
        self.create_uv_maps(mesh)
        obj = bpy.data.objects.new(f"{self.object_to_evaluate.name}_VAT", mesh)
        context.collection.objects.link(obj)
        self.base_object = obj
        return obj
