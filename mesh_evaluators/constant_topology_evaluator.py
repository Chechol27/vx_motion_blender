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

    def create_uv_maps(self, ev_mesh: bpy.types.Mesh):
        """
        Creates an uv map every 1024 vertices without separating polygons, these go from left to right and start at Y=0
        :param ev_mesh: evaluated mesh for modification
        """
        uv_map_count = -1
        loop_counter = 0
        layer_name = ""
        for v_id, vertex in enumerate(ev_mesh.vertices):
            if loop_counter >= 1024 or uv_map_count < 0:
                x_limit = min(1024, len(ev_mesh.vertices) - v_id)
                loop_counter = 0
                uv_map_count += 1
                layer_name = f"VAT_{uv_map_count}"
                try:
                    ev_mesh.uv_layers.remove(ev_mesh.uv_layers[layer_name])
                except Exception as e:
                    print(f"Creating new uv layer ({layer_name})")
                self.uv_layers.append((x_limit, ev_mesh.uv_layers.new(name=layer_name, do_init=False)))
            ev_mesh.uv_layers[layer_name].data[v_id].uv = Vector((loop_counter/x_limit, 0))
            loop_counter += 1
