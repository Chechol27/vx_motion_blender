import abc
import bpy
import numpy


class MeshEvaluator(abc.ABC):
    evaluated_meshes: [bpy.types.Mesh] = []
    object_to_evaluate: bpy.types.Object = None
    uv_layers: [bpy.types.MeshUVLoopLayer]
    base_object: bpy.types.Object
    frame_range: (int, int)

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        pass

    @abc.abstractmethod
    def evaluate_position_data(self) -> numpy.ndarray:
        pass

    @abc.abstractmethod
    def evaluate_normal_data(self) -> numpy.ndarray:
        pass

    @abc.abstractmethod
    def evaluate_tangent_data(self) -> numpy.ndarray:
        pass
