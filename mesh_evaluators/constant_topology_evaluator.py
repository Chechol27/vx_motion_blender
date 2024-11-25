import math
import bpy
import numpy

from .mesh_evaluator import MeshEvaluator
from mathutils import Vector


class ConstantTopologyEvaluator(MeshEvaluator):
    """
    Evaluated mesh collection from an object which animation has a constant topology
    useful for rigged meshes , soft bodies, ocean, clothes, etc
    """
    evaluated_meshes: [bpy.types.Mesh] = []
    object_to_evaluate: bpy.types.Object = None
    uv_layers: list[bpy.types.MeshUVLoopLayer]
    base_object: bpy.types.Object
    frame_range: (int, int)

    def __init__(self, context: bpy.types.Context, object_to_evaluate: bpy.types.Object, frame_range: (int, int)):
        super().__init__(context, object_to_evaluate, frame_range)
        self.frame_range = frame_range
        self.evaluated_meshes = []
        self.object_to_evaluate = object_to_evaluate
        for i in range(self.frame_range):
            context.scene.frame_set(i)
            deps_graph = context.evaluated_depsgraph_get()
            eval_obj = object_to_evaluate.evaluated_get(deps_graph)
            self.evaluated_meshes.append(eval_obj.data)
            if i == 0:
                self.create_base_object(context)

    def create_base_object(self, context: bpy.types.Context):
        mesh = self.evaluated_meshes[0]
        mesh.name = f"{self.object_to_evaluate.name}_VAT"
        self.create_uv_maps(mesh)
        obj = bpy.data.objects.new(f"{self.object_to_evaluate.name}_VAT", mesh)
        context.collection.objects.link(obj)
        self.base_object = obj
        return obj

    def create_uv_maps(self, ev_mesh: bpy.types.Mesh):
        """
        Creates an uv map every 1024 vertices without separating polygons, these go from left to right and start at Y=0
        :param ev_mesh: evaluated mesh for modification
        """
        uv_map_count = 0
        loop_counter = 0
        for poly in ev_mesh.polygons:
            if loop_counter >= 1020:
                loop_counter = 0
                uv_map_count += 1
            layer_name = f"VAT_{uv_map_count}"
            try:
                ev_mesh.uv_layers.remove(ev_mesh.uv_layers[layer_name])
            except Exception as e:
                print(f"Creating new layer ({id})")
            self.uv_layers.append(ev_mesh.uv_layers.new(name=layer_name))
            for loop_id in poly.loop_indices:
                ev_mesh.uv_layers[layer_name][loop_id].uv = Vector((loop_counter/1024, 0))
                loop_counter += 1

    def evaluate_position_data(self) -> numpy.ndarray:
        for layer in self.uv_layers:

        pass

    def evaluate_normal_data(self) -> numpy.ndarray:
        pass

    def evaluate_tangent_data(self) -> numpy.ndarray:
        pass

