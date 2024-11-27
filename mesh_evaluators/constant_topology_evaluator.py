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

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)

    def create_base_object(self, context: bpy.types.Context):
        mesh = self.evaluated_meshes[0]
        self.create_uv_maps(mesh)
        obj = bpy.data.objects.new(f"{self.object_to_evaluate.name}_VAT", mesh)
        context.collection.objects.link(obj)
        self.base_object = obj
        return obj
